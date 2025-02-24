import { useState } from "react";
import { Login } from "./Login";
import { Register } from "./Register"
import { ChatBox } from "./Chatbox";

/**
 * The main application component.
 * @component
 * @name App
 * @returns {JSX.Element} The rendered component.
 * @property {boolean} isLoginSuccess The logged in status of the user.
 * @property {boolean} isRegistrationComplete The registration status of the user.
 * @property {boolean} showRegister Toggle to show registration component/module.
 * @property {Function} setIsLoginSuccess The function to update the login state.
 * @property {Function} setIsRegistrationComplete The function to update the registration status.
 * @property {Function} setShowRegister The function to update the toggle for showing register comnponent/module.
 * @example
 * return <App />;
 */
function App() {
    const [isLoginSuccess, setIsLoginSuccess] = useState(false);
    const [isRegistrationComplete, setIsRegistrationComplete] = useState(false);
    const [showLogin, setShowLogin] = useState(false);
    const [showRegister, setShowRegister] = useState(false);

    const handleRegisterClick = () => {
        setShowRegister(true);
        setShowLogin(false);
    };

    const handleLoginClick = () => {
        setShowLogin(true);
        setShowRegister(false);
    };

    return (
        <div className="flex flex-col h-screen w-screen bg-gray-900 text-white">
            {isLoginSuccess && (
                <ChatBox />
            )}
            {!isLoginSuccess && !showRegister && !showLogin && !isRegistrationComplete && (
                <div>
                    <button className="bg-blue-500 text-white p-2 rounded mt-3 hover:bg-blue-700" onClick={handleLoginClick}>Login</button> / 
                    <button className="bg-blue-500 text-white p-2 rounded mt-3 hover:bg-blue-700" onClick={handleRegisterClick}>Register</button>
                </div>
            )}
            {showRegister && (
                <Register onClose={()=>{
                    setShowRegister(false);
                }} onRegistrationComplete={() => {
                    setIsRegistrationComplete(true);
                }} />
            )}
            {(showLogin) && (
                <Login onLoginSuccess={() => {
                    setIsLoginSuccess(true);
                    setIsRegistrationComplete(false);
                    setShowRegister(false);
                    setShowLogin(false);
                }} onClose={()=>{
                    setShowLogin(false);
                }} />
            )}
        </div>
    );
}

export default App;