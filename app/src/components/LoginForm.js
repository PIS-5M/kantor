import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function LoginForm(){
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [loggingError, setLoggingError] = useState('');
    const navigate = useNavigate();

    const handleLoginChange = (event) => {
        setLogin(event.target.value);
        setLoggingError('');
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
        setLoggingError('');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/login', {
                login: login, password: password
            });

            if(response.data.message === 'Login successful'){
                // Reset form
                setLogin('');
                setPassword('');
                setLoggingError('');

                // Go back to page
                navigate('/zalogowany');
            }
            else{
                // niepoprawny login lub hasło
                setLoggingError('Niepoprawny login lub hasło ');
                setLogin('');
                setPassword('');
                return;
            }

          } catch (error) {
            console.error('Error logging in:', error);
          }

    };

    return (
        <div className="flex justify-center items-center">
            <form className="p-8 bg-indigo-300 rounded shadow-lg mt-20 " onSubmit={handleSubmit}>
                <h2 className="text-2xl font-bold mb-6 ">Logowanie</h2>

                <div className="mb-4">
                    <label htmlFor="login" className="block mb-1">
                        Login:
                    </label>
                    <input
                        type="text"
                        id="login"
                        className="w-full border rounded px-3 py-2"
                        value={login}
                        onChange={handleLoginChange}
                        required
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="password" className="block mb-1">
                        Hasło:
                    </label>
                    <input
                        type="password"
                        id="password"
                        className="w-full border rounded px-3 py-2"
                        value={password}
                        onChange={handlePasswordChange}
                        required
                    />

                {loggingError && <p className="text-red-500 py-2">{loggingError}</p>}

                </div>
                <div className="flex justify-end">
                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Zaloguj
                    </button>
                </div>
            </form>

        </div>
    );
};

export default LoginForm;