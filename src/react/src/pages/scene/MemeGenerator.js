import React, {useState} from 'react';

import Credits from './Credits.js'

import Button from '../../lcars/Button.js'

const MemeGenerator = ({ep, ms, currImg, title, scene}) => {

    const content = scene ? scene.content : '';
    const [ memeText, setMemeText ] = useState( content )

    const handleTextChange = (event) => {
        let txt = event.target.value;
        setMemeText(txt);
    }

    return (
        <div className="flex m-auto">
            <div className="w-1/2">
                <div className="flex flex-shrink w-640px relative">
                    <img src={currImg} alt={ms} width="640" height="480"/>
                    <pre className="absolute bottom-5 overflow-hidden font-meme w-full text-center text-4xl text-white" >
                        {memeText}
                    </pre>
                </div>
            </div>
            <div className="w-1/2">
                <Credits ep={ep} title={title} ms={ms} />
                <p className='mt-8'>{content}</p>
                <div>
                    <textarea
                        className="mt-10 h-32 border-2 w-64 rounded-lg border-blue-600 text-lg text-white bg-blue-900 bg-opacity-50"
                        onChange={handleTextChange}
                        value={memeText}
                        placeholder="Enter Meme Text"
                    />
                </div>
                <Button className="mt-5">
                    GENERATE
                </Button>
            </div>
        </div>
    )
}

//  font-size: 48px;
//  text-transform: uppercase;
//  bottom: 32px;

export default MemeGenerator;
