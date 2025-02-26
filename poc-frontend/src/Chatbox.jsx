import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, PhoneCall } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGemoji from "remark-gemoji";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import 'katex/dist/katex.min.css';
import 'highlight.js/styles/github.css';


/**
 * The main chatbox component.
 * @component
 * @name ChatBox
 * @returns {JSX.Element} The rendered component.
 * @property {Array<String>} messages The messages history of the user.
 * @property {String} input The message/input prompt to send to the LLM.
 * @property {boolean} loading The loading status of the application.
 * @property {}
 * @property {Function} setMessages The function to update the message history.
 * @property {Function} setInput The function to update the input prompt.
 * @property {Function} setLoading The function to update the loading status.
 * @example
 * return <ChatBox />;
 */
const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const latestMessageRef = useRef(null);
    /**
     * Sends a message to the backend API and updates the messages state.
     * Gets the reply and adds/appends the reply to the messages.
     * @name sendMessage
     * @async
     * @function
     * @returns {Promise<void>}
     */
    const sendMessage = async () => {
        if (!input.trim()) return;
        const newMessages = [...messages, { role: "user", text: input }];

        setMessages(newMessages);
        setInput("");
        setLoading(true);

        try {
            const token = localStorage.getItem('access_token').toString();
            const response = await axios.post("http://localhost:5000/api/llm",
                { 
                    message: input,
                    user_id: localStorage.getItem("user_id")
                 },
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
            latestMessageRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const inputPrompt = document.getElementById("input-prompt");
    if(inputPrompt){
        inputPrompt.addEventListener("keypress", function(event) {
            if(event.key == "Enter"){
                document.getElementById("send-button").click();
            }
        });
    }

    /**
     * Initiates a call to a technician by sending a request to the backend API.
     * @name callTechnician
     * @async
     * @function
     * @returns {Promise<void>}
     */
    const callTechnician = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.post("http://localhost:5000/api/call-technician", 
                {}, 
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert(response.data.message || "Calling technician...");
        } catch (error) {
            console.error("Error initiating call:", error);
        }
    };

    return (
        <div className="flex flex-col h-screen w-screen bg-gray-900 text-white">
            <div className="flex-auto overflow-y-auto p-4 bg-gray-800">
                {messages.map((msg, index) => (
                    <div key={index}
                        ref={index === messages.length - 1 ? latestMessageRef : null}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        <span className={`px-4 py-2 rounded-lg text-sm border m-5 ${msg.role === "user" ? "bg-blue-500 border-blue-700 text-white mr-3" : "bg-gray-700 border-gray-500 text-white ml-3"}`}>
                            <ReactMarkdown
                                remarkPlugins={[remarkGemoji, remarkMath]}
                                rehypePlugins={[rehypeKatex, rehypeHighlight, rehypeRaw, rehypeSlug, rehypeAutolinkHeadings]} 
                            >
                                {msg.text}
                            </ReactMarkdown>
                        </span>
                    </div>
                ))}
            </div>
            <div className="bg-gray-800 flex gap-2 border-t border-gray-700">
                <input
                    value={input}
                    id="input-prompt"
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-auto p-2 border border-gray-600 rounded-lg bg-gray-700 text-white ml-3"
                    disabled={loading}
                />
                <button onClick={sendMessage} id="send-button" disabled={loading} className="p-2 bg-blue-500 mr-3 text-white rounded-lg flex items-center justify-center">
                    <Send className="w-5 h-5" />
                </button>
            </div>
            <button onClick={callTechnician} className="m-3 p-4 bg-green-500 text-white flex items-center rounded-lg justify-center gap-2 border-t border-green-700">
                <PhoneCall className="w-5 h-5" /> Call Technician
            </button>
        </div>
    );
}

export { ChatBox };