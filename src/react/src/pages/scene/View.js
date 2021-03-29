import React from 'react';

import Credits from './Credits.js'
import SceneCaption from './SceneCaption.js'
import Button from '../../lcars/Button.js'

const View = ({ep, ms, data, activateMemeMode}) => {

    const { scene = {}, title, img_url: currImg } = data;
    const { prev_content: prevContent = '', content = '', next_content: nextContent = ''} = scene || {};

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
