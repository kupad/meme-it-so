import React, {useState} from 'react';
import { useHistory } from "react-router-dom";


import Credits from './Credits.js'
import SceneCaption from './SceneCaption.js'
import Button from '../../lcars/Button.js'

const MemeEditor = ({ep, ms, data, activateViewMode}) => {
    const { frame: currFrame, title, scene } = data;
    const { prev_content: prevContent = '', content = '', next_content: nextContent = ''} = scene || {};

    const history = useHistory();
    const [ memeText, setMemeText ] = useState( content );

    const memeUrl = `/meme/${ep}/${currFrame.toString().padStart(5,'0')}.jpg?txt=${encodeURIComponent(memeText)}`

    /* handlers */

    //when the meme input box changes
    const onMemeChange = (event) => setMemeText(event.target.value);

    //when the generate button is pressed
    const onGenerate = () => {
        history.push(`/meme/ep/${ep}/${currFrame.toString().padStart(5,'0')}/t/${encodeURIComponent(memeText)}`)
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
