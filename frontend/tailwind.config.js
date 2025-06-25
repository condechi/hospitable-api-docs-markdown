/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",         // This is where your Tailwind classes are now
    "./src/**/*.{js,ts}",   // Add more here later as needed
  ],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/typography')],
}
