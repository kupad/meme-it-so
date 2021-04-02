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

/*
ThumbnailNav:
  -The Nav is going to display {nitems}. Each item is a thumbnail of a particular frame.
  -show every {nframes} frame. In other words, skipping nframes at a time
  -The aim is to have the currFrame in the center of the list of thumbs
  -The smallest frame is 0. The largest frame is {maxframe}
  -item->frame is item*nframes
*/

import React, { useState } from 'react';
import { Link } from "react-router-dom";

const nframes = 6; //every nth frame

const ThumbnailNav = ({ep, data: {frame: currFrame, fps, maxframe}}) => {

    //const {frame: currFrame, fps, maxframe } = data;
    const [ thumbs, setThumbs] = useState([])

    //viewport width.
    const vpwidth = window.innerWidth;
    //console.log('vpwidth', vpwidth);

    //nitems is the number of thumbs to show in the nav
    //keeping nitems odd. choose number based on screen size
    const nitems = vpwidth < 640 ? 3 : vpwidth <= 768 ? 5 : 7;
    //const nitems = 39;


    //Generate Thumbnails
    //If we have a currFrame, but the thumbs is null, we generate the thumbs now.
    if(currFrame >= 0 && thumbs.length === 0) {
        //we're keeping the currently viewed item in the center of the nav.
        //naround is the number of items to the left and right of the current shown item (normally)
        //but When currFrame is within naround items to the 0th frame or the maxframe, currFrame will not be centered
        const naround = Math.floor(nitems/2);

        //1) Calculate right boundary. We want it to be naround items to the right of the currFrame, or naround*nframes frames to to the right.
        //    But need to be careful not to go past maxframe
        const lastFrame  = Math.min(maxframe, currFrame + (naround*nframes));
        //2) Calculcate the left boundary from the right boundary. firstFrame is {nitems-1} items to the left of lastFrame, or (nitems-1)*nframes to the left
        //    As an extra precaution, make sure firstFrame isnt smaller than 0
        const firstFrame = Math.max(0, lastFrame - (nitems-1)*nframes);

        //build the array and add to the imgUrls
        const imgUrls = [];
        for(let i=0; i < nitems; i++) {
            imgUrls.push(firstFrame + (i*nframes))
        }
        setThumbs(imgUrls);
    }

    const shift = Math.floor(nitems/2); //number of items to shift left and right. looks familiar, but independent

    //given a frame, return ms offset
    const frame2ms = (frame) => {
        return Math.round(frame / fps * 1000);
    }

    const onClickPrevThumbs = () => {
        //we normally shift {shift} items at a time.
        //but if we're within {shift} items to the front, we can't go more than {distance}
        const firstFrame = thumbs[0]
        if(firstFrame === 0) return;

        const distance = firstFrame / nframes;
        const s = Math.min(shift, distance); //actual shift

        setThumbs(thumbs.map(frame => {
            return frame - s*nframes
        }))
    }
    const onClickNextThumbs = () => {
        //we normally shift {shift} items at a time.
        //but if we're within {shift} items to the end, we can't go more than {distance}
        const lastFrame = thumbs[thumbs.length - 1]
        if(lastFrame === maxframe) return;
        const distance = (maxframe - lastFrame) / nframes;
        const s = Math.min(shift, distance);

        setThumbs(thumbs.map(frame => {
            return frame + s*nframes
        }))
    }

    /* Given S03E15 return S03 */
    const getSeason = (ep) => {
        return ep.substring(0,3);
    }

    /* thumnail controls */

    return (
        <div className='flex flex-wrap justify-center mt-20 align-middle content-center items-center'>
            <button className='bg-yellow-500 h-10 rounded-l-full text-xl text-black mr-2 py-2 px-5' onClick={onClickPrevThumbs} >
                PREV
            </button>
            {
                thumbs.map(frame => (
                    <Link key={frame} to={`/scene/ep/${ep}/${frame2ms(frame)}`} >
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
