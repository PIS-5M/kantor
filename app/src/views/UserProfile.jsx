import React from 'react'
import UserData from '../components/UserData'
import Wallets from "../components/Wallets";
import AddNewWallet from '../components/AddNewWallet';

function UserProfile () {
    return (
        <div className="BLUE_BG">
          <UserData />
          <div className='mb-12'></div>
          <div className='whiteTextStyle'>Twoje portfele</div>
          <AddNewWallet />
          <div className='mb-12'></div>
          <Wallets />
        </div>
      );
}

export default UserProfile