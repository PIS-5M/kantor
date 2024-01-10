import React from 'react'
import UserData from '../components/UserData'
import Wallets from "../components/Wallets";

function UserProfile () {
    return (
        <div className="BLUE_BG">
          <UserData />
          <Wallets />
        </div>
      );
}

export default UserProfile