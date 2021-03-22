import React, { useState, useEffect } from 'react';

import Api from '../../api.js';
import StandBy from '../../lcars/StandBy.js';

import View from './View.js'
import ThumbnailNav from './ThumbnailNav.js'


const Scene = ({match: {params : {ep, ms}}}) => {
    const [ searching, setSearching ] = useState(true);
    const [ data, setData ] = useState({});

    //fetch data for this ep/ms
    useEffect(() => {
        setSearching(true);
        Api.searchByTime(ep, ms).then(result => {
            setData(result);
            setSearching(false)
        });
    }, [ep, ms]);

    const {frame: currFrame, scene, img_url: currImg, title } = data;
    const fps = 23.976023976023978; //FIXME: fps will need to come from the server

    if(!currFrame) {
        return <div></div>;
    }

    return (
        <div className="w-11/12 mx-auto mt-10">
            { searching && <StandBy /> }
            <View ep={ep} ms={ms} scene={scene} currImg={currImg} title={title} />
            <ThumbnailNav
                ep={ep}
                currFrame={currFrame}
                fps={fps}
            />
        </div>
    )

};

export default Scene;
