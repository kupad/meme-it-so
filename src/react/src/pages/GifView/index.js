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

import React, {useState, useEffect} from 'react';
import { useHistory } from "react-router-dom";

import Api from '../../api.js';
import Button from '../../lcars/Button.js'
import ButtonMedium from '../../lcars/ButtonMedium.js'
import StandBy from '../../lcars/StandBy.js'
import {staticImgUrl, padFrame} from '../../utils.js'

//const encode = (s) => {
//    return urlsafe_btoa(s);
//}

const GifView = ({match: {params : {ep, startframe, endframe, txt: enctxt = ''}}}) => {
    const history = useHistory();

    const [ generating, setGenerating ] = useState('true');
    const [ base64gif, setBase64Gif] = useState('');

    const gifUrl = `/api/gif/ep/${ep}/${padFrame(startframe)}.${padFrame(endframe)}.gif?txt=${enctxt}`
    console.log('enctxt: ', enctxt)
    console.log('gifUrl: ', gifUrl)

    const placeholder = staticImgUrl(ep,startframe)

    useEffect(() => {
        //setSearching(true);
        Api.genGif(ep, startframe, endframe, enctxt).then(respgif => {
            //setData(result);
            //setSearching(false)
            console.log('gif', respgif)
            setBase64Gif(respgif);
            setGenerating(false)
        });
    }, [ep, startframe, endframe, enctxt]);


    //TODO:
    //  - don't wrap the anchors in the button
    return (
        <div className="flex flex-wrap w-full justify-center">
            <div className='hidden sm:flex sm:flex-col sm:items-center mr-2'>
                { !generating &&
                    <>
                        <Button className='my-5 w-32 rounded-r-none'><a href={gifUrl} rel="noopener noreferrer" download>SAVE</a></Button>
                        <Button className='my-5 w-32 rounded-r-none'><a href={gifUrl} rel="noopener noreferrer" target='_blank'>VIEW</a></Button>
                    </>
                }
                <Button onClick={history.goBack} className='hidden sm:inline my-5 w-32 rounded-r-none'>BACK</Button>
            </div>
            <div className='relative'>
                <a href={gifUrl} target='_blank' rel="noopener noreferrer">
                    <img
                        src={base64gif ? `data:image/jpeg;base64,${base64gif}`: placeholder}
                        className={!base64gif ? 'opacity-50' : ''}
                        alt=''
                        width="480"
                        height="360"/>
                </a>
                { generating && <div className='absolute bottom-0'><StandBy /></div> }
            </div>
            <div className='w-full sm:hidden' />
            <div className='sm:hidden flex flex-row items-center mt-2 space-x-2'>
                { !generating &&
                    <>
                        <ButtonMedium className=''><a href={gifUrl} rel="noopener noreferrer" download>SAVE</a></ButtonMedium>
                        <ButtonMedium className=''><a href={gifUrl} rel="noopener noreferrer" target='_blank'>VIEW</a></ButtonMedium>
                    </>
                }
                { <ButtonMedium onClick={history.goBack} className='sm:hidden'>BACK</ButtonMedium> }
            </div>
        </div>
    )
}

export default GifView;
