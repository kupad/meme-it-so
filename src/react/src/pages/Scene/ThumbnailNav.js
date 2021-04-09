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

import React, { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";

import { staticImgUrl, frame2ms, nframes } from '../../utils.js'

const ThumbnailNav = ({isMultiselect=false, bounds, onBoundChange=(s,e)=>{}, nitems, ep, data: {frame: currFrame, fps, maxframe}}) => {
    const history = useHistory();

    const [ thumbs, setThumbs] = useState([])

    const calcMid = (bounds) => {
        const a = Math.floor((bounds.start + bounds.end) / 2);
        return a - Math.floor(a%nframes);
    }

    const mid = bounds ? calcMid(bounds) : -1;

        /*
    useEffect(() => {
        //if(thumbs.length > 0 && !bounds ) {
            onBoundChange({
                 start: thumbs[0],
                 end: thumbs[thumbs.length -1],
                 reprFrame: thumbs[0],
            })
        //}
    }, []);
    */

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
        const frames = [];
        for(let i=0; i < nitems; i++) {
            frames.push(firstFrame + (i*nframes))
        }
        setThumbs(frames);
    }

    //const shift = Math.floor(nitems/2); //number of items to shift left and right. looks familiar, but independent
    const shift = 3; //number of items to shift left and right. looks familiar, but independent

    //see previous thumbs
    const onClickPrevThumbs = () => {
        //we normally shift {shift} items at a time.
        //but if we're within {shift} items to the front, we can't go more than {distance}
        const firstFrame = thumbs[0]
        if(firstFrame === 0) return;

        const distance = firstFrame / nframes;
        const s = Math.min(shift, distance); //actual shift

        const nthumbs = thumbs.map(frame => {
            return frame - s*nframes
        })
        setThumbs(nthumbs);

        //bounds are never off view. also has the effect of never going over nitems long
        if(isMultiselect)
            onBoundChange({
                start: Math.max(nthumbs[0], bounds.start),
                end: Math.min(nthumbs[nthumbs.length-1], bounds.end),
                reprFrame: Math.min(nthumbs[0], bounds.start),
            })
    }

    //see next thumbs
    const onClickNextThumbs = () => {
        //we normally shift {shift} items at a time.
        //but if we're within {shift} items to the end, we can't go more than {distance}
        const lastFrame = thumbs[thumbs.length - 1]
        if(lastFrame === maxframe) return;

        const distance = (maxframe - lastFrame) / nframes;
        const s = Math.min(shift, distance);

        const nthumbs = thumbs.map(frame => {
            return frame + s*nframes
        })
        setThumbs(nthumbs);

        //bounds are never off view. also has the effect of never going over nitems long
        if(isMultiselect)
            onBoundChange({
                start: Math.max(nthumbs[0], bounds.start),
                end: Math.min(nthumbs[nthumbs.length-1], bounds.end),
                reprFrame: Math.min(nthumbs[0], bounds.start),
            })
    }

    //when isMultiselect, this is wat we run, to choose what thumbs are selected
    //based on what was clicked.
    //Goal:
    //  --if we're left of the current midpoint, add to the left
    //  --if we're right of the current midpoint, add to the right
    const selectOnClick = (frame) => {
        const changeStart = frame < mid;
        console.log(frame)
        console.log(mid)

        const nbounds = changeStart
            ? { start: frame, end: bounds.end, reprFrame: frame}
            : { start: bounds.start, end: frame, reprFrame: bounds.start}

        onBoundChange(nbounds);
    }

    //change currently selected frame based on what was clicked
    const changeOnClick = (frame) => {
        history.push(`/scene/ep/${ep}/${frame2ms(frame,fps)}`);
    }

    const onThumbClick = isMultiselect ? selectOnClick : changeOnClick;

    //is the given frame currently selected?
    const isSelected = (frame) => {
        const rv = (isMultiselect && bounds)
            ? frame >= bounds.start && frame <= bounds.end
            : frame === currFrame;
        //console.log('isSelected:', 'frame', frame, rv, 'multisel', isMultiselect, 'bounds', bounds);
        return rv;
    }

    /* thumnail controls */

    return (
        <div className='flex flex-wrap justify-center align-middle content-center items-center'>
            <button className='bg-yellow-500 h-10 rounded-l-full text-xl text-black mr-2 py-2 px-5' onClick={onClickPrevThumbs} >
                PREV
            </button>
            {
                thumbs.map(frame => (
                    <img
                        key={frame}
                        className={`p-2 ${ isSelected(frame) ? 'border-2 border-yellow-500' : ''} ${ frame===mid ? 'border-4' : ''}`}
                        src={staticImgUrl(ep,frame)} width="160" height="120"
                        alt=''
                        onClick={()=>onThumbClick(frame)}
                    />
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
