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
const Login = ({ onLoginSuccess, onClose }) => {
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
            const response = await axios.post('http://localhost:5000/api/auth/login', { emailId:email, password:password });
            console.log(response.data["access_token"]);
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
                        className='w-full p-2 border border-gray-300 rounded mt-1'
                        type="email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        className='w-full p-2 border border-gray-300 rounded mt-1'
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>
                {error && <p className="error text-red-500 mt-2">{error}</p>}
                <button onClick={onClose} className='bg-red-500 text-white p-2 rounded mt-3 hover:bg-red-700'>Cancel</button>
                <button type="submit" className='bg-blue-500 text-white p-2 rounded mt-3 hover:bg-blue-700'>Login</button>
            </form>
        </div>
    );
};

export { Login };
