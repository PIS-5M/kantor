export default function clientToken() {

    const login = (id) => {
          sessionStorage.setItem('userId', JSON.stringify(id));    }

    const logout = () => {
      sessionStorage.removeItem('userId')
        }

  const userId = () => {
      const tokenString = sessionStorage.getItem('userId');
      if (tokenString) {
          const userData = JSON.parse(tokenString);
          return userData;
    }
    return null;
  }

    return {login, logout, userId}
  }