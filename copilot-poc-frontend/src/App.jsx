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
    const [showRegister, setShowRegister] = useState(false);

    const handleRegisterClick = () => {
        setShowRegister(true);
    };

    const handleLoginClick = () => {
        setShowRegister(false);
    };

    return (
        <div>
            {isLoginSuccess && <ChatBox />}
            {!isLoginSuccess && !showRegister && (
                <div>
                    <button onClick={handleLoginClick}>Login</button>
                    <button onClick={handleRegisterClick}>Register</button>
                </div>
            )}
            {!isLoginSuccess && showRegister && <Register onRegistrationComplete={() => setIsRegistrationComplete(true)} />}
            {!isLoginSuccess && !showRegister && isRegistrationComplete && (
                <Login onLoginSuccess={() => {
                    setIsLoginSuccess(true);
                    setIsRegistrationComplete(false);
                }} />
            )}
        </div>
    );
}

export default App;