import React from "react";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

export const DialogMatches = ({ isOpen, data, toggle }) => {
  return (
    <div>
      <Modal isOpen={isOpen} toggle={toggle}>
        <ModalHeader toggle={toggle}>Zmatchowane Oferty</ModalHeader>
        <ModalBody>
          {data && data.length > 0 ? (
            <ul>
              {data.map((match, index) => (
                <li key={index}>
                  Sprzedano: {match[0]} waluty, Zarobiono: {match[1]}
                </li>
              ))}
            </ul>
          ) : (
            <p>Nie znaleziono pasujących ofert 💔</p>
          )}
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={toggle}>
            Zamknij
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
};
