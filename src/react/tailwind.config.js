module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
        fontFamily: {
            'meme': [ 'Impact', 'Arial', 'sans-serif' ],
            'sttng-credits': ['OPTICristeta-Italic', 'serif'],
            'sttng-lcars': [ 'Okuda', 'sans-serif' ],
        },
        width: {
            '640px': '640px',
            '95': '95%',
            '96': '96%',
            '97': '97%',
            '98': '98%',
            '99': '99%',
        },
        height: {
            '480px': '480px'
        }

    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
