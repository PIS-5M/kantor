import React from "react";

export const DialogMatches = ({ data, onClose }) => {
  // TODO styling
  return (
    <div className="dialog-window">
      <h3>Zmatchowane Oferty</h3>
      <ul>
        {data.map((match, index) => (
          <li key={index}>
            Sprzedano: {match[0]} waluty, Zarobiono: {match[1]}
          </li>
        ))}
      </ul>
      <button onClick={onClose}>Zamknij</button>
    </div>
  );
};
