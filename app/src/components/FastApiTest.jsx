import React, { useEffect, useState } from "react";


const FastContext = React.createContext({
  messages: [], fetchMessages: () => {}
})

export default function FastApiTest() {
  const [messages, setMessages] = useState([])
  const fetchMessages = async () => {
    const response = await fetch("http://localhost:8000/messages")
    const messages = await response.json()
    setMessages(messages.data)
  }

  useEffect(() => {
    fetchMessages()
  }, [])
  return (
    <FastContext.Provider value={{messages, fetchMessages}}>
        {messages.map((m) => (
          <p key={m.id}>{m.item}</p>
        ))}
    </FastContext.Provider>
  )
}