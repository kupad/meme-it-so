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
import React, { useState, useEffect } from 'react';

import Api from '../../api.js';
import StandBy from '../../lcars/StandBy.js';

import View from './View.js'
import MemeEditor from './MemeEditor.js'
import ThumbnailNav from './ThumbnailNav.js'
import {useHistoryState} from '../../hooks.js'

const Mode = {
    VIEW: 'VIEW',
    MEME: 'MEME',
}

const Scene = ({match: {params : {ep, ms}}}) => {

    const [ searching, setSearching ] = useState(true);
    const [ mode, setMode] = useHistoryState('mode', Mode.VIEW);
    const [ data, setData ] = useState({});

    //console.log('ep', ep, 'ms', ms, 'data', data)

    //fetch data for this ep/ms
    useEffect(() => {
        setSearching(true);
        Api.searchByTime(ep, ms).then(result => {
            setData(result);
            setSearching(false)
        });
    }, [ep, ms]);

    const {frame: currFrame, scene, img_url: currImg, title, fps, maxframe } = data;

    if(!(currFrame >= 0)) {
        return <div></div>;
    }

    const activateMemeMode = () => setMode(Mode.MEME);
    const activateViewMode = () => setMode(Mode.VIEW);

    return (
        <div className="w-11/12 mx-auto mt-10">
            { searching && <StandBy /> }
            {
                mode === Mode.MEME
                    ? <MemeEditor ep={ep} ms={ms} data={data} activateViewMode={activateViewMode}/>
                    : <View ep={ep} ms={ms} data={data} activateMemeMode={activateMemeMode} />
            }
            <ThumbnailNav ep={ep} data={data}  />
        </div>
    )

};

export default Scene;
