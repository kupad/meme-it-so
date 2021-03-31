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

import { Link } from "react-router-dom";

const Credits = ({ep, title, ms, eplink=true}) => {

    /* Given S03E15 return 03 */
    const getSeasonNum = (ep) => {
        return ep.substring(1,3);
    }

    /* Given S03E15 return 15 */
    const getEpisodeNum = (ep) => {
        return ep.substring(4);
    }

    const toTimeStr = (ms) => {
        const totseconds = (ms / 1000);
        const m = Math.round(totseconds / 60);
        const s = Math.floor(totseconds % 60).toString().padStart(2,'0')
        return `${m}:${s}`;
    }

    return (
        <div className="mt-5 md:mt-0">
            <div className="mb-2 font-sttng-credits text-blue-sttng-credits">
                { title && <h1 className="md:text-3xl word-spacing-xl">"{title}"</h1> }
                <h2 className="md:text-lg">
                    Season <span className="tracking-tighter">{getSeasonNum(ep)}</span> / Episode <span className="tracking-tighter">{getEpisodeNum(ep)}</span>
                        {ms && <span className="tracking-tighter">&nbsp;&nbsp;&nbsp;&nbsp;({toTimeStr(ms)})</span>}
                </h2>
            </div>
            { eplink && <Link to={`/episode/ep/${ep}`} className='text-sm px-3 py-1 bg-yellow-500 text-black rounded-full'>VIEW EPISODE</Link> }
        </div>
    );
}

export default Credits;
