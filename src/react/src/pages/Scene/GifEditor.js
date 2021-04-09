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

import React, {useState} from 'react';
import { useHistory } from "react-router-dom";

import ThumbnailNav from './ThumbnailNav.js'
import Button from '../../lcars/Button.js'
import ButtonMedium from '../../lcars/ButtonMedium.js'
import ButtonSmall from '../../lcars/ButtonSmall.js'
import {useHistoryState} from '../../hooks.js'
import { frame2ms, padFrame, staticImgUrl} from '../../utils.js'
import {urlsafe_btoa} from '../../utils.js'

const nitems=39;

const GifEditor = ({ep, startms, data, activateViewMode}) => {

    const {fps, scene, frame: currFrame} = data;

    console.log('scene: ', scene)

    const { content = '' } = scene || {};

    const history = useHistory();
    const [bounds, setBounds] = useState({ start: currFrame, end: currFrame, reprFrame: currFrame });
    const [ memeText, setMemeText ] = useHistoryState('gifMemeText', content);
    //const [ memeText, setMemeText ] = useState(content);

    console.log('memeText: ', memeText)
    console.log('bounds: ', bounds)

    const onGenerate = () => {
        history.push(`/gif/ep/${ep}/sf/${padFrame(bounds.start)}/ef/${padFrame(bounds.end)}/t/${urlsafe_btoa(memeText)}`)
    }

    const updateBounds = (b) => {
        setBounds(b);
    }

    //total time of selected frames
    const totalTime = bounds
        ? Math.max(0,(frame2ms(bounds.end, fps) - frame2ms(bounds.start,fps)) / 1000)
        : 0;

    //when the meme input box changes
    const onMemeChange = (event) => setMemeText(event.target.value);

    const imgUrl = (reprFrame,memeText) => {
        return memeText
            ? `/api/meme/${ep}/${reprFrame.toString().padStart(5,'0')}.jpg?txt=${urlsafe_btoa(memeText)}`
            : staticImgUrl(ep,reprFrame);
    }

    return (
        <div>
            <div className='flex space-x-6 items-center mb-3'>
                <div className="border flex-grow-0">
                    { bounds &&
                        //<img src={`/api/gif/ep/${ep}/${bounds.start}.${bounds.end}.gif`} width="320" alt='' />
                        <img src={imgUrl(bounds.reprFrame,memeText)} width="320" height="240" alt='' />
                    }
                </div>
                <div className='h-56 relative flex flex-col justify-start'>
                    <textarea
                        className="block h-32 border-2 w-72 rounded-lg border-blue-600 font-meme text-lg text-white bg-blue-900 bg-opacity-50"
                        placeholder="Enter Meme Text (optional)"
                        onChange={onMemeChange}
                        value={memeText}
                    >
                    </textarea>
                    <div className='flex space-x-2 mt-2'>
                        <ButtonMedium className="" disabled={totalTime < 1} onClick={onGenerate}>GENERATE</ButtonMedium>
                        <ButtonMedium className="" onClick={activateViewMode}>CANCEL</ButtonMedium>
                    </div>
                    <div className='flex-grow-1' />
                    <div className='absolute bottom-0'>{totalTime} seconds</div>
                </div>
            </div>
            <ThumbnailNav ep={ep} data={data} isMultiselect={true} bounds={bounds} onBoundChange={updateBounds} nitems={nitems} />
        </div>
    )
}

export default GifEditor;
