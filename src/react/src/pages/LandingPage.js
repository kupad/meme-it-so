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

import React from 'react';

const LandingPage = () => (
    <div className='text-center text-yellow-500'>
        <h1 className='text-6xl xl:text-7xl'>ACCESS GRANTED</h1>
        <div className='my-10'>
            <img className='mx-auto w-1/2 lg:w-1/5' src='United_Federation_of_Planets_logo.svg' alt='UFP' />
        </div>
        <ul className='text-center text-3xl'>
            <li className=''>STTNG SCREENCAP DATABANK LINK READY</li>
            <li className=''>MEME GENERATOR ONLINE</li>
            <li className=''>AWAITING QUERY PARAMETERS</li>
        </ul>
    </div>
)

export default LandingPage;
