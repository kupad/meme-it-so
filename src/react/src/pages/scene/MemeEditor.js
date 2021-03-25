import React, {useState} from 'react';

import Credits from './Credits.js'
import ThumbnailNav from './ThumbnailNav.js'

import Button from '../../lcars/Button.js'

const MemeEditor = ({ep, ms, fps, currFrame, title, scene, activateViewMode}) => {

    const content = scene ? scene.content : '';
    const [ memeText, setMemeText ] = useState( content );
    const [ amEditing, setAmEditing ] = useState(true);

    const memeUrl = generateMemeUrl(ep, currFrame, memeText)

    const handleTextChange = (event) => setMemeText(event.target.value);
    const handleGenerate = () => setAmEditing(false);
    const handleBackToEditor = () => setAmEditing(true)

    return (
        <>
            {
                amEditing
                    ? <EditView
                            ep={ep}
                            ms={ms}
                            fps={fps}
                            currFrame={currFrame}
                            content={content}
                            title={title}
                            memeText={memeText}
                            memeUrl={memeUrl}
                            onTextChange={handleTextChange}
                            onGenerate={handleGenerate}
                            activateViewMode={activateViewMode}
                        />
                    : <GeneratedView
                            currFrame={currFrame}
                            memeUrl={memeUrl}
                            onBack={handleBackToEditor}
                        />
            }
        </>
    )
}

const generateMemeUrl = (ep, frame, txt) => (
    `/meme/${ep}/${frame.toString().padStart(5,'0')}.jpg?txt=${encodeURIComponent(txt)}`
)

const EditView = ({ep, ms, fps, currFrame, title, content, memeText, memeUrl, onTextChange, onGenerate, activateViewMode}) => {
        return (
            <>
            <div className="flex m-auto">
                <div className="w-1/2">
                     <img src={memeUrl} alt={currFrame} width="640" height="480"/>
                </div>
                <div className="w-1/2 ml-5">
                    <Credits ep={ep} title={title} ms={ms} />
                    <p className='mt-8'>{content}</p>
                    <div>
                        <textarea
                            className="mt-10 h-32 border-2 w-80 rounded-lg border-blue-600 text-lg text-white bg-blue-900 bg-opacity-50"
                            onChange={onTextChange}
                            value={memeText}
                            placeholder="Enter Meme Text"
                        />
                    </div>
                    <div className='flex'>
                        <Button className="mt-5" onClick={onGenerate}>
                            GENERATE
                        </Button>
                        <Button className="mt-5 ml-10" onClick={activateViewMode}>
                            CANCEL
                        </Button>
                    </div>
                </div>
            </div>
            <ThumbnailNav
                ep={ep}
                currFrame={currFrame}
                fps={fps}
            />
            </>
        )
}

const GeneratedView = ({memeUrl, currFrame, onBack}) => {
    return (
        <div className="flex w-full justify-start">
            <div className='flex flex-col items-center mr-2'>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} download>SAVE</a></Button>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} target='_blank'>VIEW</a></Button>
                <Button onClick={onBack} className='my-5 w-32 rounded-r-none'>BACK</Button>
            </div>
            <div>
                <a href={memeUrl} target='_blank'><img className='' src={memeUrl} alt={currFrame} width="640" height="480"/></a>
            </div>
        </div>
    )
}

export default MemeEditor;
