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
const SceneCaption = ({prev, curr, next}) => {
    //if(!curr)
    //    return <div className="h-32"></div>

    return (
        <div className="mt-10">
            <pre className='text-white text-opacity-50'>{prev}</pre>
            <pre>{curr ? curr : '...'}</pre>
            <pre className='text-white text-opacity-50'>{next}</pre>
        </div>
    )
}

export default SceneCaption;
