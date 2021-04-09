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

const About = () => (
    <div>
        <h1 className="text-center text-7xl">ABOUT</h1>
        <div className='w-1/2 space-y-2 mx-auto font-serif'>
            <p>Use "Meme It So" to find screen captures from <span className='font-bold'>Star Trek: The Next Generation</span> and
            generate memes. Yes, it's clearly inspired by the wonderful <a className='text-blue-500' href="https://frinkiac.com/">Frinkiac</a>!</p>

            <p><span class="font-bold">NOTE:</span>As of right now, I'm working on improving the screencapture and text capture data.
                Many episodes are out of sync.</p>

            <h5 className='font-bold text-2xl'>License Notice:</h5>

            <p>"Meme It So" is a media (TV show and movies) screen capture and text caption
            database and image macro generator.</p>
            <p>Copyright &copy; 2021  Phillip Dreizen</p>

            <p>Meme It So is free software: you can redistribute it and/or modify
            it under the terms of the GNU Affero General Public License as published
            by the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.</p>

            <p>Meme It So is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
            See the GNU Affero General Public License for more details.</p>

            <p>A copy of the GNU Affero General Public License is available for <a className='text-blue-500' href='LICENSE'>download here</a> or can
            be <a className='text-blue-500' href="https://www.gnu.org/licenses/agpl-3.0.en.html">viewed here.</a></p>

            <p>Source is available here: <a className='text-blue-500' href="https://github.com/kupad/meme-it-so">https://github.com/kupad/meme-it-so</a>.</p>

        </div>
    </div>
)

export default About;
