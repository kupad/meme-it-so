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

import React from 'react';
import { useHistory } from "react-router-dom";

import SceneCaption from './SceneCaption.js'
import Credits from '../../components/Credits/'
import Button from '../../lcars/Button.js'
import {useHistoryState} from '../../hooks.js'
import {urlsafe_btoa} from '../../utils.js'

const encode = (s) => {
    return urlsafe_btoa(s);
}

const MemeEditor = ({ep, ms, data, activateViewMode}) => {
    const history = useHistory();

    const { frame: currFrame, title, prevScene, scene, nextScene } = data;

    //get the prev, current, and next captions
    const { content: prevContent = '' } = prevScene || {};
    const { content = '' } = scene || {};
    const { content: nextContent = '' } = nextScene || {};

    const [ memeText, setMemeText ] = useHistoryState( 'memeText', content);

    const memeUrl = `/meme/${ep}/${currFrame.toString().padStart(5,'0')}.jpg?txt=${encode(memeText)}`

    //when the meme input box changes
    const onMemeChange = (event) => setMemeText(event.target.value);

    //when the generate button is pressed
    const onGenerate = () => {
        history.push(`/meme/ep/${ep}/${currFrame.toString().padStart(5,'0')}/t/${encode(memeText)}`)
    }

    return (
        <div className="md:flex m-auto">
            <div className="md:w-1/2">
                 <img src={memeUrl} alt={currFrame} width="640" height="480"/>
            </div>
            <div className="md:w-1/2 ml-5">
                <Credits ep={ep} title={title} ms={ms} />
                <SceneCaption prev={prevContent} curr={content} next={nextContent} />
                <div>
                    <textarea
                        className="mt-7 h-32 border-2 w-72 rounded-lg border-blue-600 font-meme text-lg text-white overflow-y-scroll bg-blue-900 bg-opacity-50"
                        onChange={onMemeChange}
                        value={memeText}
                        placeholder="Enter Meme Text"
                    />
                </div>
                <div className='flex'>
                    <Button className="mt-5" disabled={!memeText} onClick={onGenerate}>GENERATE</Button>
                    <Button className="mt-5 ml-10" onClick={activateViewMode}>CANCEL</Button>
                </div>
            </div>
        </div>
        )
}

export default MemeEditor;
