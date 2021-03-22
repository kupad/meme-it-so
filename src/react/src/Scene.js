import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";

import Api from './api.js';
import StandBy from './lcars/StandBy.js';

//const thumbnails='/stactic/thumnails/'

/* thumnail controls */
const nitems = 7; //keep it odd
const nframes = 6; //every nth frame

/* Given S03E15 return S03 */
const getSeason = (ep) => {
    return ep.substring(0,3);
}

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

//FIXME: fps will need to come from the server

const fps = 23.976023976023978;
const frame2ms = (frame) => {
    return Math.round(frame / fps * 1000);
}

const Scene = ({match: {params : {ep, ms}}}) => {
    //shall I wrap this stuff up in a single object? It's looking
    //like that is what I ought to do
    const [ searching, setSearching ] = useState(true);
    const [ scene, setScene ] = useState(null)
    const [ currFrame, setCurrFrame] = useState(0)
    const [ currImg, setCurrImg ] = useState('')
    const [ thumbs, setThumbs] = useState([])
    const [ title, setTitle] = useState('')

    useEffect(() => {
        Api.searchByTime(ep, ms).then(result => {
            setScene(result.scene)
            setCurrFrame(result.frame)
            setCurrImg(result.img_url)
            setTitle(result.title)
            setSearching(false)
            console.log(result.frame)
            if(result.frame) {
                const imgUrls = []
                let firstFrame = result.frame - (Math.floor(nitems/2)*nframes)
                let lastFrame = result.frame + (Math.floor(nitems/2)*nframes)
                const imgs = []
                for(let i=firstFrame; i<=lastFrame; i+=nframes) {
                    imgUrls.push(i)
                }
                setThumbs(imgUrls);
            }

        });
    }, [ep, ms]);
console.log('currFrame', currFrame)
    if(!currFrame) {
        return <div></div>;
    }

    const prevThumbs = () => {
        setThumbs(thumbs.map(frame => {
            return frame - Math.floor(nitems/2)*nframes
        }))
    }
    const nextThumbs = () => {
        setThumbs(thumbs.map(frame => {
            return frame + Math.floor(nitems/2)*nframes
        }))
    }

    return (
        <div className="w-11/12 mx-auto mt-10">
            { searching && <StandBy /> }
            <div className="flex m-auto">
                <div className="w-1/2">
                    <img src={currImg} width="640" height="480"/>
                </div>
                <div className="w-1/2">
                    <div className="font-serif italic text-blue-sttng-credits">
                        <h1 className="text-3xl">"{title}"</h1>
                        <h2 className="text-lg">Season {getSeasonNum(ep)} / Episode {getEpisodeNum(ep)} ({toTimeStr(ms)})</h2>
                    </div>
                    <pre className="mt-10">
                        {scene ? scene.content : ''}
                    </pre>
                </div>
            </div>
            <div className='flex justify-center mt-20 align-middle content-center items-center'>
                <button
                    className='bg-yellow-500 h-10 rounded-full font-bold text-black py-2 px-10'
                    onClick={prevThumbs}
                >
                        -003
                </button>
                {
                    thumbs.map(frame => (
                        <Link
                            key={frame}
                            to={`/scene/ep/${ep}/${frame2ms(frame)}`}
                        >
                            <img
                                className={`p-2 ${frame === currFrame ? 'border-2 border-yellow-500' : ''}`}
                                src={`/static/thumbnails/${getSeason(ep)}/${ep}/${frame.toString().padStart(5,'0')}.jpg`} width="160" height="120"/>
                        </Link>
                    ))
                }
                <button
                    className='bg-yellow-500 h-10 rounded-full font-bold text-black py-2 px-10'
                    onClick={nextThumbs}
                >
                    +003
                </button>
            </div>
        </div>
    )

};

export default Scene;
