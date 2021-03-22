import React, { useState, useEffect } from 'react';

import Api from '../../api.js';
import StandBy from '../../lcars/StandBy.js';

import ThumbnailNav from './ThumbnailNav.js'

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

const Scene = ({match: {params : {ep, ms}}}) => {
    const [ searching, setSearching ] = useState(true);
    const [ data, setData ] = useState({});

    useEffect(() => {
        setSearching(true);
        Api.searchByTime(ep, ms).then(result => {
            setData(result);
            setSearching(false)
        });
    }, [ep, ms]);

    const {frame: currFrame, scene, img_url: currImg, title } = data;

    if(!currFrame) {
        return <div></div>;
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
            <ThumbnailNav
                ep={ep}
                currFrame={currFrame}
                fps={fps}
            />
        </div>
    )

};

export default Scene;
