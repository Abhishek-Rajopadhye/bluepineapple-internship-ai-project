/* eslint-disable react/prop-types */
import { useState } from 'react';
import axios from 'axios';


/**
 * The Component that handles the login and auth of the user.
 * @component
 * @name Login
 * @returns {JSX.Element} The rendered Component.
 * @prop {Function} onLoginSuccess The function from parent component to handle actions after login success.
 * @property {String} email The emailID of the user.
 * @property {String} password The password of the user.
 * @property {String} error. The error message on error in execution of application.
 * @property {Function} setEmail The function to update the emailID on change in input box.
 * @property {Function} setPassword The function to update the password on change in input box.
 * @property {Function} setError The function to set the error message on error.
 */
const Login = ({ onLoginSuccess }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    /**
     * The function that handles the communication with the backend on submit of login form.
     * @function
     * @name handleSubmit
     * @param {Event} event
     * @returns {void}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('/login', { email, password });
            console.log(response.data);
            const { access_token } = response.data["access_token"];
            localStorage.setItem('access_token', access_token);
            onLoginSuccess();
            // Redirect or perform other actions after successful login
        } catch (error) {
            console.log(error)
            setError('Invalid email or password')
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export {Login};
