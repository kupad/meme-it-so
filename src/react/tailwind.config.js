/*
This file is part of Meme It So

"Meme It So" is a media (TV show and movies) screen capture and text caption
database and image macro generator.
Copyright (C) 2021  Phillip Dreizen

Meme It So is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Meme It So is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
        fontFamily: {
            'meme': [ 'Impact', 'Arial', 'sans-serif' ],
            'sttng-title': [ 'TNG_Title' ],
            'sttng-credits': ['OPTICristetaItalic' ],
            'sttng-lcars': [ 'Swiss911UltraCompressed' ],
            /* 'sttng-lcars': [ 'Okuda', 'sans-serif' ], */
        },
        width: {
            '28ch': '28ch',
            '160px': '160px',
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
