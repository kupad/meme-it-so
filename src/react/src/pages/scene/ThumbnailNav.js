import React, { useState } from 'react';
import { Link } from "react-router-dom";

const ThumbnailNav = ({ep, fps, currFrame}) => {

    const [ thumbs, setThumbs] = useState([])

    const nitems = 7; //keep it odd
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
                className='bg-yellow-500 h-10 rounded-l-full font-bold text-black mr-2 py-2 px-5'
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
                className='bg-yellow-500 h-10 rounded-r-full font-bold text-black ml-2 py-2 px-5'
                onClick={onClickNextThumbs}
            >
                NEXT
            </button>
        </div>
    );
}

export default ThumbnailNav;
