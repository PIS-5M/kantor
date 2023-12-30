import React, { useState } from 'react';
import {
  Input,
  InputGroup,
  Button,
  Form,
  FormFeedback,
} from 'reactstrap';
import axios from 'axios';

function RegistrationForm() {
  const [registrationError, setRegistrationError] = useState("")
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    email: '',
    password: '',
    repeatedPassword: '',
    validate: {
      nameState: '',
      surnameState: '',
      emailState: '',
      passwordState: '',
      repeatedPasswordState: ''
    }
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
        name: formData.name, surname: formData.surname,
        password: formData.password, email: formData.email
      });

    } catch (error) {
      console.error('Error registration', error);
    }
    window.location.href = '/logowanie';
  };

  const isEmailTaken = async (event, email) => {
    try {
        const response = await axios.post('http://localhost:8000/email_used', {
          email: email,

        });
        return(response.data.message)


      } catch (error) {
      };
    };

  const keysToCheck = ['nameState','surnameState', 'emailState', 'passwordState', 'repeatedPasswordState']

  const isValid = () => {
    if(keysToCheck.every(key => formData.validate[key] === "has-success")) return true;
    return false;
  }

  const isNameValid = (e) => {
    const { validate, ...userData} = formData;
    const regex = /^(?:[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]* ?)+$/;
    if (!(regex.test(e.target.value))) {
      validate.nameState = 'has-danger';
    } else {
      validate.nameState = 'has-success';
    }
    setFormData({validate, ...userData})
  }

  const isSurnameValid = (e) => {
    const { validate, ...userData} = formData;
    const regex = /^[A-ZŁŚŻ][a-ząćęłńóśźż]+([-][A-ZŁŚŻ][a-ząćęłńóśźż]+)?$/;
    if (!(regex.test(e.target.value))) {
      validate.surnameState = 'has-danger';
    } else {
      validate.surnameState = 'has-success';
    }
    setFormData({validate, ...userData})
  }

  const isEmailValid = (e) => {
    const emailRex =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const { validate, ...userData} = formData;

    if (emailRex.test(e.target.value)) {
      validate.emailState = 'has-success';
    } else {
      validate.emailState = 'has-danger';
    }

    setFormData({ validate, ...userData });
        }

  const isPasswordValid = (e) => {
    const { validate, ...userData } = formData;
    console.log(formData);
    if (
      e.target.value.length >= 8 &&
      /[A-Z]/.test(e.target.value) &&
      /[a-z]/.test(e.target.value) &&
      /[0-9]/.test(e.target.value) &&
      /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(e.target.value)
    ) {
      validate.passwordState = 'has-success';
    } else {
      validate.passwordState = 'has-danger';
    }

    setFormData({ validate, ...userData });
  }

  const isRepeatedPasswordValid = (e) => {
    console.log(formData);
    const {validate, ...userData } = formData;
    if (e.target.value === formData.password) {
      validate.repeatedPasswordState = 'has-success';
    } else {
      validate.repeatedPasswordState = 'has-danger';
    }

    setFormData({ validate, ...userData });
  }


  return(
    <div className="loginFormPos">
<div className="registrationForm">
    <h1 className="textLogin">Zarejestruj się</h1>
    <Form>
        <InputGroup className="inputGroup">
            <Input className="centeredTextInput" maxLength={50} placeholder="Imię" name="name" value={formData.name}
                                                valid={formData.validate.nameState === 'has-success'}
                                                invalid={formData.validate.nameState === 'has-danger'}
                                                onChange={(ev) => { isNameValid(ev); handleChange(ev)}} />
          <FormFeedback>Wprowadź swoje imię.</FormFeedback>
        </InputGroup>
        <InputGroup className="inputGroup">
            <Input className="centeredTextInput" maxLength={50} placeholder="Nazwisko" name="surname" value={formData.surname}
                                                valid={formData.validate.surnameState === 'has-success'}
                                                invalid={formData.validate.surnameState=== 'has-danger'}
                                                onChange={(ev) => {isSurnameValid(ev); handleChange(ev)}}/>
        <FormFeedback>Wprowadź swoje nazwisko.</FormFeedback>
        </InputGroup>
        <InputGroup className="inputGroup">
            <Input className="centeredTextInput" maxLength={50} placeholder="Adres e-mail" name="email" value={formData.email}
                                                valid={formData.validate.emailState === 'has-success'}
                                                invalid={formData.validate.emailState=== 'has-danger'}
                                                onChange={(ev) => {isEmailValid(ev); handleChange(ev); setRegistrationError("")}}/>
        <FormFeedback>Wprowadź poprawny adres e-mail.</FormFeedback>
        </InputGroup>
        <InputGroup className="inputGroup">
            <Input className="centeredTextInput" type="password" maxLength={50} placeholder="Hasło" name="password" value={formData.password}
                                                valid={formData.validate.passwordState === 'has-success'}
                                                invalid={formData.validate.passwordState=== 'has-danger'}
                                                onChange={(ev) => {isPasswordValid(ev); handleChange(ev)}}/>
        <FormFeedback>Hasło musi zawierać co najmniej 8 znaków, małą i wielką literę, cyfrę oraz znak specjalny.</FormFeedback>
        </InputGroup>
        <InputGroup className="inputGroup">
            <Input className="centeredTextInput" type="password" maxLength={50} placeholder="Powtórz hasło" name="repeatedPassword" value={formData.repeatedPassword}
                                                valid={formData.validate.repeatedPasswordState === 'has-success'}
                                                invalid={formData.validate.repeatedPasswordState=== 'has-danger'}
                                                onChange={(ev) => {isRepeatedPasswordValid(ev); handleChange(ev)}}/>
        <FormFeedback>Wprowadzone hasła nie są identyczne.</FormFeedback>
        </InputGroup>
        <label className="errorLabel">{registrationError}</label>
    </Form>
    <div>
        <Button
            className="buttonStyleLoginUser whiteTextStyle" type="submit" onClick={async (e) =>
              {let isTaken = await isEmailTaken(e, formData.email);
              if(!isTaken) {handleSubmit(e)}
              else {setRegistrationError("Konto o podanym adresie e-mail już istnieje.")}}} disabled={!isValid()} >
        ZAREJESTRUJ SIĘ
        </Button>
    </div>
</div></div>
)

}


export default RegistrationForm;