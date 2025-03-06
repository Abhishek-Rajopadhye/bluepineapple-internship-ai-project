import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send } from "lucide-react";
import { Message } from "./Message";
import { CallButton } from "./CallButton";

/**
 * The main chatbox component.
 * @component
 * @name ChatBox
 * @returns {JSX.Element} The rendered component.
 * @example
 * return <ChatBox />;
 */
const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const latestMessageRef = useRef(null);

    const fetchPreviousMessages = async () => {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:8000/api/llm/history",
            { headers: { Authorization: `Bearer ${token}` } })
        
            if(response.status != 200){
            throw new Error("Network Error");
        }

        const history = response.data["history"].map((item) => ({
            text: item.content,
            role: item.role
        }));
        setMessages(history);
    };

    const sendMessage = async () => {
        if (!input.trim()) return;
        const newMessages = [...messages, { role: "user", text: input }];

        setMessages(newMessages);
        setInput("");
        setLoading(true);

        try {
            const token = localStorage.getItem("access_token");
            const response = await axios.post(
                "http://localhost:8000/api/llm",
                { message: input, user_id: localStorage.getItem("user_id") },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setMessages([...newMessages, { role: "llm", text: response.data.reply }]);
        } catch (error) {
            console.error("Error fetching response:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (latestMessageRef.current) {
            latestMessageRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    useEffect(() => {
        fetchPreviousMessages();
    }, []);

    return (
        <div className="flex flex-col h-screen w-screen bg-gray-900 text-white">
            <div className="flex-auto overflow-y-auto p-4 bg-gray-800">
                {messages.map((msg, index) => (
                    <Message key={index} msg={msg} ref={index === messages.length - 1 ? latestMessageRef : null} />
                ))}
            </div>
            <div className="bg-gray-800 flex gap-2 border-t border-gray-700">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-auto p-2 border border-gray-600 rounded-lg bg-gray-700 text-white ml-3"
                    disabled={loading}
                />
                <button onClick={sendMessage} disabled={loading} className="p-2 bg-blue-500 mr-3 text-white rounded-lg flex items-center justify-center">
                    <Send className="w-5 h-5" />
                </button>
            </div>
            <CallButton />
        </div>
    );
};

export { ChatBox };