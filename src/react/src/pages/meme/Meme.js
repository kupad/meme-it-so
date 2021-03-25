import React from 'react';
import { useHistory } from "react-router-dom";

import Button from '../../lcars/Button.js'

const Meme = ({match: {params : {ep, frame, txt}}}) => {
    const history = useHistory();

    //TODO: repeated in the MemeEditor. factor out
    const memeUrl = `/meme/${ep}/${frame.toString().padStart(5,'0')}.jpg?txt=${encodeURIComponent(txt)}`

    //TODO:
    //  - don't wrap the anchors in the button
    //  - preserve state on back
    return (
        <div className="flex w-full justify-center">
            <div className='flex flex-col items-center mr-2'>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} download>SAVE</a></Button>
                <Button className='my-5 w-32 rounded-r-none'><a href={memeUrl} target='_blank'>VIEW</a></Button>
                <Button onClick={history.goBack} className='my-5 w-32 rounded-r-none'>BACK</Button>
            </div>
            <div>
                <a href={memeUrl} target='_blank'><img className='' src={memeUrl} alt={frame} width="640" height="480"/></a>
            </div>
        </div>
    )
}

export default Meme;
