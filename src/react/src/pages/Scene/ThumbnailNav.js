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
import React, { useState } from 'react';
import { Link } from "react-router-dom";

const ThumbnailNav = ({ep, fps, currFrame}) => {

    const [ thumbs, setThumbs] = useState([])

    const vpwidth = window.innerWidth;
    console.log(vpwidth);

    //keep nitems odd. choose number based on screen size
    const nitems = vpwidth < 640 ? 3 : vpwidth <= 768 ? 5 : 7;

    const nframes = 6; //every nth frame
    const frame2ms = (frame) => {
        return Math.round(frame / fps * 1000);
    }

    //If we have a currFrame, but the thumbs is null, we generate
    //the thumbs now. Could this go into initial state? But it only works if
    //the currFrame is >0
    if(currFrame && thumbs.length === 0) {
        let firstFrame = currFrame - (Math.floor(nitems/2)*nframes)
        let lastFrame = currFrame + (Math.floor(nitems/2)*nframes)
        const imgUrls = []
        for(let i=firstFrame; i<=lastFrame; i+=nframes) {
            imgUrls.push(i)
        }
        if(imgUrls.length > 0) {
            setThumbs(imgUrls);
        }
    }

    const onClickPrevThumbs = () => {
        setThumbs(thumbs.map(frame => {
            return frame - Math.floor(nitems/2)*nframes
        }))
    }
    const onClickNextThumbs = () => {
        setThumbs(thumbs.map(frame => {
            return frame + Math.floor(nitems/2)*nframes
        }))
    }

    /* Given S03E15 return S03 */
    const getSeason = (ep) => {
        return ep.substring(0,3);
    }

    /* thumnail controls */

    return (
        <div className='flex justify-center mt-20 align-middle content-center items-center'>
            <button
                className='bg-yellow-500 h-10 rounded-l-full text-xl text-black mr-2 py-2 px-5'
                onClick={onClickPrevThumbs}
            >
                PREV
            </button>
            {
                thumbs.map(frame => (
                    <Link
                        key={frame}
                        to={`/scene/ep/${ep}/${frame2ms(frame)}`}
                    >
                        <img
                            className={`p-2 ${frame === currFrame ? 'border-2 border-yellow-500' : ''}`}
                            src={`/static/thumbnails/${getSeason(ep)}/${ep}/${frame.toString().padStart(5,'0')}.jpg`} width="160" height="120"
                            alt=''
                        />
                    </Link>
                ))
            }
            <button
                className='bg-yellow-500 h-10 rounded-r-full text-xl text-black ml-2 py-2 px-5'
                onClick={onClickNextThumbs}
            >
                NEXT
            </button>
        </div>
    );
}

export default ThumbnailNav;
