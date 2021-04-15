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
import React, { useState } from 'react';

import { Switch, Route, Link, useHistory } from "react-router-dom";

import api from '../../api.js'
import {bp2pix} from '../../utils.js'

import LCARSBar from '../../lcars/LCARSBar.js'
import ButtonMedium from '../../lcars/ButtonMedium.js'

import LandingPage from '../LandingPage/'
import Scene from '../Scene/'
import Meme from '../Meme/'
import GifView from '../GifView/'
import Search from '../Search/'
import About from '../About/'
import Episode from '../Episode/'
import NotFound from '../NotFound/'


function App() {
    const history = useHistory();

    const [ searchTerm, setSearchTerm ] = useState('');

    const handleSearchChanged = (event) => {
        //console.log(searchTerm)
        setSearchTerm(event.target.value)
    }

    const handleSearch = (event) => {
        if(searchTerm) {
            history.push(`/search/${searchTerm}`)
        }
        event.preventDefault();
    };

    const logo = (classes = '') => (
        <div className={`float-left font-sttng-title text-blue-sttng-credits text-center text-4xl ${classes}`}>
            <span className='lg:ml-2'><Link to='/'>MEME IT SO<sub className='text-sm text-blue-100'>Alpha</sub></Link></span>
        </div>
    )

    const onRandom = () => {
        api.random().then(resp => {
            console.log(resp);
            const {scene: {ep, start}} = resp;
            history.push(`/scene/ep/${ep}/${start}`)
        });
    }

    const getPlaceholderText = () => {
        const vpwidth = window.innerWidth;
        return vpwidth >= bp2pix('sm')
            ? "search by quote (try: merry man, bird meat, make it so)"
            : "search by quote (try: merry man)";
    }

    return (
        <div className='min-h-screen mx-auto'>
            <header className='items-center mb-1'>
                <div className='w-11/12 mx-auto my-2 lg:my-3'>
                    {logo()}
                    <div className='float-right my-1'>
                        <ButtonMedium onClick={onRandom} className='bg-blue-400'>RANDOM</ButtonMedium>
                    </div>
                    <form className="clear-both flex justify-center lg:clear-none lg:px-10" onSubmit={handleSearch}>
                        <label className='hidden' htmlFor='search'>Search: </label>
                        <input
                            className='border-2 flex-grow rounded-lg border-blue-600 text-3xl text-white bg-blue-900 bg-opacity-50 lg:max-w-prose'
                            placeholder={getPlaceholderText()}
                            type='text'
                            id='search'
                            value={searchTerm}
                            onChange={handleSearchChanged}
                        />
                    <button className='hidden xl:inline bg-yellow-400 rounded-full text-black text-2xl pl-20 pt-1 pb-1 pr-4 ml-5' type='submit'>QUERY</button>
                    </form>
                    { /* TODO: unhide the random soon! */}
                    {
                      //for centering when the width gets very large
                      //logo('invisible hidden 2xl:block')
                    }
                </div>
            </header>
            <div className="w-99 mb-10 mx-auto">
                <LCARSBar msg="STAR TREK TNG MEME GENERATOR"/>
            </div>
            <Switch>
                <Route path="/" exact component={LandingPage} />
                <Route path="/About" component={About} />
                <Route path="/search/:query" component={Search} />
                <Route path="/scene/ep/:ep/:ms" component={Scene} />
                <Route path="/gif/ep/:ep/sf/:startframe/ef/:endframe/t/:txt?" component={GifView} />
                <Route path="/meme/ep/:ep/:frame/t/:txt" component={Meme} />
                <Route path="/episode/ep/:ep" component={Episode} />
                <Route component={NotFound} />
            </Switch>
        </div>
    )
}

export default App;
