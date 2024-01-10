// export default function clientToken() {
//   const login = (id) => {
//     sessionStorage.setItem("userId", JSON.stringify(id));
//   };

//   const logout = () => {
//     sessionStorage.removeItem("userId");
//   };

//   const userId = () => {
//     const tokenString = sessionStorage.getItem("userId");
//     if (tokenString) {
//       const userData = JSON.parse(tokenString);
//       return userData;
//     }
//     return null;
//   };

//   return { login, logout, userId };
// }

export default function clientToken() {
  // Mock login function
  const login = (id) => {
    console.log(`Mock login with id: ${id}`);
  };

  // Mock logout function
  const logout = () => {
    console.log("Mock logout");
  };

  // Mock userId function to always return 1
  const userId = () => {
    return 1;
  };

  return { login, logout, userId };
}
