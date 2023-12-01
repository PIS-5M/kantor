import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function RegistrationForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    login: '',
    password: '',
    email: '',
    phoneNumber: '',
    bankAccount: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/registration', {
        name: formData.name, surname: formData.surname, login: formData.login,
        password: formData.password, email: formData.email, phoneNumber: formData.phoneNumber,
        bankAccount: formData.bankAccount
      });
      console.log("Message:", response.data.message);

    } catch (error) {
      console.error('Error registration', error);
    }

    // Go to main page
    navigate('/');
  };

  return (
    <form className="max-w-md mx-auto mt-8 shadow-lg rounded p-8 bg-indigo-300" onSubmit={handleSubmit}>
      <h2 className="text-2xl font-bold mb-6">Rejestracja</h2>

      <div>
        <div className="mb-4">
          <label htmlFor="name" className="block mb-2 font-medium">
            Imię
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="surname" className="block mb-2 font-medium">
            Nazwisko
          </label>
          <input
            type="text"
            id="surname"
            name="surname"
            value={formData.surname}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="login" className="block mb-2 font-medium">
            Login
          </label>
          <input
            type="text"
            id="login"
            name="login"
            value={formData.login}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="block mb-2 font-medium">
            Hasło
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="email" className="block mb-2 font-medium">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="phoneNumber" className="block mb-2 font-medium">
            Numer telefonu
          </label>
          <input
            type="tel"
            id="phoneNumber"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
            />
        </div>

        <div className="mb-4">
          <label htmlFor="bankAccount" className="block mb-2 font-medium">
            Numer konta bankowego
          </label>
          <input
            type="text"
            id="bankAccount"
            name="bankAccount"
            value={formData.bankAccount}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded focus:outline-none focus:border-blue-500"
            required
          />
        </div>

      </div>

        <div className="flex justify-end">
            <button
                  type="submit"
                  className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
            Zarejestruj się
            </button>
        </div>
    </form>
  );}

export default RegistrationForm;