import React, { useState } from "react";
import {
    Input,
    InputGroup,
    Button,
    Form,
    FormFeedback,
  } from 'reactstrap';
  import axios from 'axios';
  import '../styles/loginStyles.css'
  import clientToken from "../ClientToken";

function LoginForm ()
{
    const [userEmail, setUserEmail] = useState("")
    const [userPassword, setUserPassword] = useState("")
    const [loggingError, setLoggingError] = useState("")
    const [validateEmail, setValidateEmail] = useState('')
    const [validatePassword, setValidatePassword] = useState('')
    const {login} = clientToken();


    const Login = async (event) =>
    {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/login', {
                email: userEmail, password: userPassword
            });
            login(response.data.id)
            window.location.href = '/'

          } catch (error) {
                setLoggingError(error.response.data.detail);}
        };

        const isValid = () => {
            if(validateEmail === "has-success" && validatePassword ==='has-success') return true;
            return false;
          }


        const handleLogin = (event) =>{
            if(isValid() === false) {return};
            Login(event);
        }

        const isEmailValid = (e) => {
            const emailRex =
              /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

            if (emailRex.test(e.target.value)) {
              setValidateEmail('has-success');
            } else {
              setValidateEmail('has-danger');
            }
                }

        const isPasswordValid = (e) =>
            {
                if ("" === e.target.value) {
                    setValidatePassword('has-danger');
                }
                else {
                setValidatePassword('has-success')}
            }


    return(
        <div className="loginFormPos">
    <div className="loginForm">
        <h1 className="textLogin">Zaloguj się</h1>
        <Form>
            <InputGroup className="inputGroup">
                <Input className="centeredTextInput" maxLength={30} placeholder="Adres e-mail"
                                                    valid={validateEmail === 'has-success'}
                                                    invalid={validateEmail === 'has-danger'}
                                                    onChange={ev => { setUserEmail(ev.target.value); isEmailValid(ev); setLoggingError("")}} />
                <FormFeedback>Wprowadź poprawny adres e-mail.</FormFeedback>
            </InputGroup>
            <InputGroup className="inputGroup">
                <Input className="centeredTextInput" maxLength={30} type="password" placeholder="Hasło"
                                                    valid={validatePassword === 'has-success'}
                                                    invalid={validatePassword === 'has-danger'}
                                                    onChange={ev => {setUserPassword(ev.target.value); isPasswordValid(ev); setLoggingError("")}}/>
            <FormFeedback>Wprowadź swoje hasło.</FormFeedback>
            </InputGroup>
            <label className="errorLabel">{loggingError}</label>
        </Form>
        <div>
            <Button
                className="buttonStyleLoginUser whiteTextStyle" onClick={handleLogin}
            >
            ZALOGUJ SIĘ
            </Button>
        </div>
    </div></div>
    )

}

export default LoginForm;