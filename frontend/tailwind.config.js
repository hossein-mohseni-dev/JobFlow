/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#10211f",
        mist: "#f4f7f6",
        pine: "#0f766e",
        sand: "#e7efe9",
      },
    },
  },
  plugins: [],
};
