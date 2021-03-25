import React from 'react';

import Credits from './Credits.js'
import ThumbnailNav from './ThumbnailNav.js'

import Button from '../../lcars/Button.js'

const View = ({ep, ms, fps, currFrame, currImg, title, scene, activateMemeMode}) => {

    return (
        <div className="flex m-auto">
            <div className="w-1/2">
                <img src={currImg} alt={ms} width="640" height="480"/>
            </div>
            <div className="w-1/2 ml-5">
                <Credits ep={ep} title={title} ms={ms} />
                {
                    scene
                        ? <pre className="mt-10 h-32">{scene.content}</pre>
                        : <div className="h-32"></div>
                }
                <Button onClick={activateMemeMode}>MEME EDITOR</Button>
            </div>
        </div>
    )
}

export default View;
