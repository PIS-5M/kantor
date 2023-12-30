import React from 'react';
import {
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
} from 'reactstrap';
import "../styles/headerStyles.css";
import clientToken from '../ClientToken.js';


function Header() {
  const {userId} = clientToken();

  return (
    <div>
      <Nav pills className='headerStyle'>
        <NavbarBrand>
                <img src="./logokantor.png" alt="Logo"></img>
        </NavbarBrand>
        <NavItem className='buttonStyleHeader'>
          <NavLink
            href="./" className='textStyle'>
            Kursy walut
          </NavLink>
        </NavItem>
        <NavItem className='buttonStyleHeader'>
          <NavLink href="./" className='textStyle'>
            Kalkulator walutowy
          </NavLink>
        </NavItem>
        {userId() ? (<><NavItem className='buttonStyleHeader'>
                                            <NavLink href="./oferty" className='textStyle'>
                                                Aktywne oferty
                                            </NavLink>
                                            </NavItem>
                                            <NavItem className='buttonStyleHeader'>
                                            <NavLink href="./onas" className='textStyle'>
                                                O nas
                                            </NavLink>
                                            </NavItem></>
                                            )
                                            : (
                                            <><NavItem className='buttonStyleHeader'>
                                            <NavLink href="./onas" className='textStyle'>
                                                O nas
                                            </NavLink>
                                            </NavItem>
                                            <NavItem className='buttonStyleHeader'>
                                            <NavLink href="./logowanie" className='textStyle'>
                                                Zaloguj się
                                            </NavLink>
                                            </NavItem>
                                            <NavItem className='registrationButtonStyle'>
                                            <NavLink href="./rejestracja" className='whiteTextStyle'>
                                                Zarejestruj się
                                            </NavLink>
                                            </NavItem></>)
    }


      </Nav>
    </div>
  );
}

export default Header;
