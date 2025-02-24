/* eslint-disable react/prop-types */
import { useState } from 'react';
import axios from 'axios';

/**
 * The component that handles the registration of users.
 * @component
 * @name Register
 * @returns {JSX.Element} The rendered component.
 * @prop {Function} onRegistrationComplete The function from parent component to handle actions on registration completion.
 * @property {String} emailId The emailID of the user.
 * @property {String} password The password of the user.
 * @property {String} confirmPassword The confirmation for the password.
 * @property {String} error. The error message on error in execution of application.
 * @property {Function} setEmailId The function to update the emailID on change in input box.
 * @property {Function} setPassword The function to update the password on change in input box.
 * @property {Function} setConfirmPassword The function to update the confirmPassword on change in input box.
 * @property {Function} setError The function to set the error message on error.
 */
const Register = ({onRegistrationComplete}) => {
    const [emailId, setEmailId] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');

    /**
     * The function that handles the communication with the backend on submit of registration form.
     * @function
     * @name handleSubmit
     * @param {Event} event
     * @returns {void}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        try {
            const response = await axios.post('/register', { emailId, password });
            console.log('Registration successful', response.data);
            onRegistrationComplete();
        } catch (error) {
            console.error('Registration failed', error);
            setError('Registration failed');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email ID:</label>
                    <input
                        type="email"
                        value={emailId}
                        onChange={(e) => setEmailId(e.target.value)}
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
                <div>
                    <label>Confirm Password:</label>
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(event) => setConfirmPassword(event.target.value)}
                        required
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export { Register };