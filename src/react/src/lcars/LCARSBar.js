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


const LCARSBar = ({msg}) => (
    <div className="flex h-9 w-full">
        <div className="bg-purple-400 mr-2 w-10 rounded-l-full" />
        <div className="bg-purple-400 mr-2 w-1/5" />
        <div className="bg-yellow-500 mr-2 w-10" />
        <div className="bg-purple-400 mr-2 w-1/6" />
        <div className="bg-purple-400 mr-2 flex-grow" />
        {
            msg &&
            <div className="hidden md:block md:text-3xl lg:text-4xl ml-5 mr-5 text-yellow-500 ">
                {msg}
            </div>
        }
        <div className="bg-purple-400 mr-2 w-10 rounded-r-full" />
    </div>
);

export default LCARSBar;
