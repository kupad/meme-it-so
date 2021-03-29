import React from 'react';

import Credits from './Credits.js'
import Button from '../../lcars/Button.js'

const View = ({ep, ms, currImg, title, scene, activateMemeMode}) => {

    return (
        <div className="md:flex m-auto">
            <div className="md:w-1/2">
                <img src={currImg} alt={ms} width="640" height="480"/>
            </div>
            <div className="md:w-1/2 ml-5">
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
