import React, { useEffect, useState } from 'react'
import clientToken from '../ClientToken';
import axios from "axios";
import "../styles/userStyles.css";



function UserData () {
    const {userId} = clientToken();
    const [userName, setUserName] = useState("")
    const [userSurname, setUserSurname] = useState("")
    const [email, setEmail] = useState("")

    const getUserData = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/user_data", {
            id: userId()
          });
          setUserName(response.data.name);
          setUserSurname(response.data.surname);
          setEmail(response.data.email);

        } catch (error) {
            console.log(error.message)
          }
      };

      useEffect((e) => {
        getUserData(e);
      }, []);

      return (
        <>
        <div className='textLogin'>
            Twój profil użytkownika
        </div>
        <div className='rectangle'>
            <div className='margin'>Imię: {userName} </div>
            <div className='margin'>Nazwisko: {userSurname} </div>
            <div className='margin'>E-mail: {email} </div>
        </div>
        </>
      )

}

export default UserData