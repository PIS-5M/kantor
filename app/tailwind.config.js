/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.jsx"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Exo 2", "sans-serif"],
      },
      colors: {
        background: {
          DEFAULT: "#d9d9d9",
        },
      },
    },
  },
  plugins: [],
};
