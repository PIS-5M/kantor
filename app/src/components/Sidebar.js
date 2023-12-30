import React from 'react';
import {
  Nav,
  NavItem,
  NavLink,
} from 'reactstrap';
import "../styles/headerStyles.css";
import clientToken from '../ClientToken';

function Sidebar () {
    const {logout} = clientToken();

    const handleLogout = () => {
        logout();
      }

    return(
    <Nav vertical className='sidebarStyle'>
  <NavItem className='sidebarPosStyle'>
    <NavLink className='textStyle' href="/moje_transakcje">
      💵 Moje transakcje
    </NavLink>
  </NavItem>
  <NavItem className='sidebarPosStyle'>
    <NavLink className='textStyle' href="/moje_oferty">
      💲 Moje oferty
    </NavLink>
  </NavItem>
  <NavItem className='sidebarPosStyle'>
    <NavLink className='textStyle' href="/dodaj">
      💸 Dodaj nową ofertę
    </NavLink>
  </NavItem>
  <NavItem className='sidebarPosStyle'>
    <NavLink className='textStyle' href="/profil">
      👱‍♀️ Mój profil
    </NavLink>
  </NavItem>
  <NavItem className='sidebarPosStyle' onClick={handleLogout}>
    <NavLink className='textStyle'>
      ❌ Wyloguj
    </NavLink>
  </NavItem>

</Nav>
    )
}

export default Sidebar;