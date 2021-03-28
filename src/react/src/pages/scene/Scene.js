import React, { useState, useEffect } from 'react';

import Api from '../../api.js';
import StandBy from '../../lcars/StandBy.js';

import View from './View.js'
import MemeEditor from './MemeEditor.js'
import ThumbnailNav from './ThumbnailNav.js'

const Scene = ({match: {params : {ep, ms}}}) => {
    const [ searching, setSearching ] = useState(true);
    const [ isMemeMode, setIsMemeMode ] = useState(false);
    const [ data, setData ] = useState({});

    //fetch data for this ep/ms
    useEffect(() => {
        setSearching(true);
        Api.searchByTime(ep, ms).then(result => {
            setData(result);
            setSearching(false)
        });
    }, [ep, ms]);

    const {frame: currFrame, scene, img_url: currImg, title, fps } = data;

    if(!currFrame) {
        return <div></div>;
    }

    const activateMemeMode = () => setIsMemeMode(true);
    const activateViewMode = () => setIsMemeMode(false);

    return (
        <div className="w-11/12 mx-auto mt-10">
            { searching && <StandBy /> }
            {
                isMemeMode
                    ? <MemeEditor ep={ep} ms={ms} fps={fps} scene={scene} currFrame={currFrame} currImg={currImg} title={title} activateViewMode={activateViewMode}/>
                    : <View ep={ep} ms={ms} scene={scene} currImg={currImg} title={title} activateMemeMode={activateMemeMode} />
            }
            <ThumbnailNav ep={ep} currFrame={currFrame} fps={fps} />
        </div>
    )

};

export default Scene;
