import { useState } from "react";
import axios from "axios";
import { Send, PhoneCall } from "lucide-react";

function App() {
const [messages, setMessages] = useState([]);
const [input, setInput] = useState("");
const [loading, setLoading] = useState(false);

const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
        const response = await axios.post("http://localhost:5000/api/copilot", { message: input });
        setMessages([...newMessages, { role: "copilot", text: response.data.reply }]);
    } catch (error) {
        console.error("Error fetching response:", error);
    } finally {
        setLoading(false);
    }
};

const callTechnician = async () => {
    try {
        const response = await axios.post("http://localhost:5000/api/call-technician");
        alert(response.data.message || "Calling technician...");
    } catch (error) {
        console.error("Error initiating call:", error);
    }
};

return (
    <div className="flex flex-col h-screen w-screen bg-gray-900 text-white">
        <div className="flex-1 overflow-y-auto p-4 bg-gray-800">
            {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <span className={`px-4 py-2 rounded-lg text-sm border ${msg.role === "user" ? "bg-blue-500 border-blue-700 text-white" : "bg-gray-700 border-gray-500 text-white"}`}>{msg.text}</span>
            </div>
            ))}
        </div>
        <div className="p-4 bg-gray-800 flex gap-2 border-t border-gray-700">
            <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 p-2 border border-gray-600 rounded-lg bg-gray-700 text-white"
                disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading} className="p-2 bg-blue-500 text-white rounded-lg flex items-center justify-center">
                <Send className="w-5 h-5" />
            </button>
        </div>
            <button onClick={callTechnician} className="w-full p-4 bg-green-500 text-white flex items-center justify-center gap-2 border-t border-green-700">
                <PhoneCall className="w-5 h-5" /> Call Technician
            </button>
    </div>
);
}

export default App;