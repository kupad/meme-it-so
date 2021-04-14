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
import { Link } from "react-router-dom";

import Button from '../../lcars/Button.js'
import StandBy from '../../lcars/StandBy.js'
import Api from '../../api.js';
import Credits from '../../components/Credits/'
import { staticSmallImgUrl, toTimeStr } from '../../utils.js'

const initialResults = {
        ep: '',
        page: 0,
        scenes: [],
        isLoading: false
};

const Episode = ({match: {params : {ep}}}) => {
    const [ results, setResults] = useState(initialResults);

    const [ trigger, setTrigger] = useState({ ep: ep, page: 1 });

    if(ep !== trigger.ep) {
        setResults(initialResults);
        setTrigger({ ep: ep, page: 1 });
    }

    useEffect(()=> {
        setResults(r => ({ ...r, isLoading: true}));
        Api.getAllScenes(trigger.ep, trigger.page).then(resp => {
            setResults(r => {
                const same = r.ep === trigger.ep && r.page === trigger.page;
                return {
                    ...resp,
                    scenes: same ? resp.scenes : [...r.scenes, ...resp.scenes],
                    isLoading: false,
                };
            })
        });
    },[trigger]);

    //handle more increments the trigger
    const handleMore = () => setTrigger(t => ({
       ...t,
        page: t.page + 1
    }))

    const {scenes, title, hasMore} = results;

    const key = (scene) => {
        return `${scene.ep}-${scene.srtidx}`;
    }

    return (
        <div className='w-10/12 mx-auto'>
            { results.isLoading && <StandBy /> }
            { results.scenes.length > 0 && <Credits ep={ep} title={title} eplink={false} /> }
            <div className='mt-5'>
                {
                    scenes && scenes.map(scene => (
                        <div key={key(scene)} className='flex flex-col sm:flex-row space-y-2 space-x-5 items-center border-t border-blue-200 py-5'>
                            <Link className='w-24 2xl:w-32 text-center' to={`/scene/ep/${ep}/${scene.start_offset}`}>
                                {toTimeStr(scene.start_offset)} - {toTimeStr(scene.end_offset)}
                            </Link>
                            <Link className='w-160px flex-shrink-0' to={`/scene/ep/${ep}/${scene.start_offset}`}>
                                <img src={staticSmallImgUrl(ep,scene.frame)} alt='' width="160" height="120"/>
                            </Link>
                            <div className='font-mono sm:w-640px'>
                                <p className='2xl:whitespace-pre'>{scene.content}</p>
                            </div>
                        </div>
                    ))
                }
                <div className='text-center my-2'>
                {
                    hasMore &&
                    <Button onClick={handleMore}>MORE</Button>
                }
                </div>

            </div>
        </div>
    )
}

export default Episode;
