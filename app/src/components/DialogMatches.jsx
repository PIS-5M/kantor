import React from "react";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

export const DialogMatches = ({ isOpen, data, toggle }) => {
  return (
    <div>
      <Modal isOpen={isOpen} toggle={toggle}>
        <ModalHeader toggle={toggle}>Zmatchowane Oferty</ModalHeader>
        <ModalBody>
          {data ? (
            <ul>
              {data.map((match, index) => (
                <li key={index}>
                  Sprzedano: {match[0]} waluty, Zarobiono: {match[1]}
                </li>
              ))}
            </ul>
          ) : (
            <p>Brak danych do wyświetlenia.</p>
          )}
        </ModalBody>
        <ModalFooter>
          <Button color="secondary" onClick={toggle}>
            Zamknij
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
};