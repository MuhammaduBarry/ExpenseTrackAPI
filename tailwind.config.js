/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"], // Adjust path as needed
  theme: {
    extend: {
      screens: {
        'custom-lg': '1279px', // Define your custom breakpoint
      },
    },
  },
  plugins: [],
}