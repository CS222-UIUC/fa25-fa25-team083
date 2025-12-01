/** @type {import('tailwindcss').Config} */
module.exports = {
  // Use class-based dark mode so we control it with `document.documentElement.classList`
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx,html}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
