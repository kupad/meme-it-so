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

import Button from '../../lcars/Button.js'
import ButtonMedium from '../../lcars/ButtonMedium.js'

const Meme = ({match: {params : {ep, frame, txt: enctxt=''}}}) => {
    const history = useHistory();

    const memeUrl = `/api/meme/${ep}/${frame.toString().padStart(5,'0')}.jpg?txt=${enctxt}`

    //TODO:
    //  - don't wrap the anchors in the button
    //  - preserve state on back
    return (
        <div className="flex flex-wrap sm:flex-no-wrap w-full justify-center">
            <div className='hidden sm:flex sm:flex-col sm:items-center sm:mr-2'>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} rel="noopener noreferrer" download>SAVE</a></Button>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} rel="noopener noreferrer" target='_blank'>VIEW</a></Button>
                <Button onClick={history.goBack} className='my-5 w-32 rounded-r-none'>BACK</Button>
            </div>
            <div>
                <a href={memeUrl} target='_blank' rel="noopener noreferrer"><img src={memeUrl} alt={frame} width="640" height="480"/></a>
            </div>
            <div className='w-full sm:hidden' />
            <div className='flex flex-row sm:items-center mt-2 space-x-2 sm:hidden'>
                <ButtonMedium className=''><a href={memeUrl} rel="noopener noreferrer" download>SAVE</a></ButtonMedium>
                <ButtonMedium className=''><a href={memeUrl} rel="noopener noreferrer" target='_blank'>VIEW</a></ButtonMedium>
                <ButtonMedium onClick={history.goBack} className=''>BACK</ButtonMedium>
            </div>
        </div>
    )
}

export default Meme;
