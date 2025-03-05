import { useState } from "react";
import axios from "axios";
import { PhoneCall } from "lucide-react";

const CallButton = () => {
    const [jitsiUrl, setJitsiUrl] = useState("");

    const callTechnician = async () => {
        try {
            const token = localStorage.getItem("access_token");
            const response = await axios.get("http://localhost:8000/api/call/call-technician", {
                headers: { Authorization: `Bearer ${token}` },
            });

            setJitsiUrl(response.data.jitsi_url);
            window.open(jitsiUrl, "_blank"); // Opens Jitsi Meet in a new tab
        } catch (error) {
            console.error("Error initiating call:", error);
        }
    };

    return (
        <button onClick={callTechnician} className="m-3 p-4 bg-green-500 text-white flex items-center rounded-lg justify-center gap-2 border-t border-green-700">
            <PhoneCall className="w-5 h-5" /> Call Technician
        </button>
    );
};

export { CallButton };
