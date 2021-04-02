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

import SceneCaption from './SceneCaption.js'
import Button from '../../lcars/Button.js'
import Credits from '../../components/Credits/'

const View = ({ep, ms, data: {prevScene, scene, nextScene, title, imgUrl: currImg}, activateMemeMode}) => {

    const { content: prevContent = '' } = prevScene || {};
    const { content = '' } = scene || {};
    const { content: nextContent = '' } = nextScene || {};

    return (
        <div className="md:flex m-auto">
            <div className="md:w-1/2">
                <img src={currImg} alt={ms} width="640" height="480"/>
            </div>
            <div className="md:w-1/2 ml-5">
                <Credits ep={ep} title={title} ms={ms} />
                <SceneCaption
                    prev={prevContent}
                    curr={content}
                    next={nextContent}
                />
            <div className='mt-7'>
                    <Button onClick={activateMemeMode}>MEME EDITOR</Button>
                </div>
            </div>
        </div>
    )
}

export default View;
