import React from "react";
import { useNavigate } from "react-router-dom";

function RegistrationButton() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/rejestracja");
  };

  return (
    <div className="flex justify-end">
      <button
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={handleClick}
      >
        Zarejestruj się
      </button>
    </div>
  );
}

export default RegistrationButton;
