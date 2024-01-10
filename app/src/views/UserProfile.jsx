import React from 'react'
import UserData from '../components/UserData'
import Wallets from "../components/Wallets";
import AddNewWallet from '../components/AddNewWallet';

function UserProfile () {
    return (
        <div className="BLUE_BG">
          <UserData />
          <AddNewWallet />
          <Wallets />
        </div>
      );
}

export default UserProfile