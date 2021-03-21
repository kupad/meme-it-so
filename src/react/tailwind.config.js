module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
        width: {
            '95': '95%',
            '96': '96%',
            '97': '97%',
            '98': '98%',
            '99': '99%',
        }

    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
