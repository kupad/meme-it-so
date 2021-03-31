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

import LCARSBar from './lcars/LCARSBar.js'
import LandingPage from './pages/LandingPage.js'
import Scene from './pages/scene/Scene.js'
import Meme from './pages/meme/Meme.js'
import Search from './Search.js' //TODO: move to pages
import About from './pages/About.js'

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

    return (
        <div className='min-h-screen mx-auto'>
            <header className='items-center h-24 xl:grid xl:grid-cols-3'>
                <div className='font-sttng-title text-blue-sttng-credits text-center text-3xl md:text-4xl 2xl:text-6xl'>
                    <span className='md:ml-5'><Link to='/'>MEME IT SO</Link></span>
                </div>
                <div className='text-center'>
                    <form className="" onSubmit={handleSearch}>
                        <label className='hidden' htmlFor='search'>Search: </label>
                        <input
                            className='border-2 w-72 rounded-lg border-blue-600 text-3xl text-white bg-blue-900 bg-opacity-50 '
                            placeholder="search by quote"
                            type='text'
                            id='search'
                            value={searchTerm}
                            onChange={handleSearchChanged}
                        />
                    <button className='hidden md:inline bg-yellow-400 rounded-full text-black text-2xl pl-20 pt-1 pb-1 pr-4 ml-5' type='submit'>QUERY</button>
                    </form>
                </div>
                <div className=''></div>
            </header>
            <div className="w-99 mb-10 mx-auto">
                <LCARSBar msg="STTNG SCREENCAP DATABASE"/>
            </div>
            <Switch>
                <Route path="/" exact component={LandingPage} />
                <Route path="/About" component={About} />
                <Route path="/search/:query" component={Search} />
                <Route path="/scene/ep/:ep/:ms" component={Scene} />
                <Route path="/meme/ep/:ep/:frame/t/:txt" component={Meme} />
            </Switch>
        </div>
    )
}

export default App;
