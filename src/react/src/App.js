import React, { useState } from 'react';

import { Switch, Route, useHistory } from "react-router-dom";

import LCARSBar from './lcars/LCARSBar.js'
import LandingPage from './pages/LandingPage.js'
import Scene from './pages/scene/Scene.js'
import Meme from './pages/meme/Meme.js'
import Search from './Search.js'

function App() {
    const history = useHistory();

    const [ searchTerm, setSearchTerm ] = useState('');

    const handleSearchChanged = (event) => {
        //console.log(searchTerm)
        setSearchTerm(event.target.value)
    }

    const handleSearch = (event) => {
        history.push(`/search/${searchTerm}`)
        event.preventDefault();
    };

    return (
        <div className='min-h-screen mx-auto'>
            <header className='items-center h-24 xl:grid xl:grid-cols-3'>
                <div className='font-sttng-title text-blue-sttng-credits text-center text-3xl md:text-4xl 2xl:text-6xl'>
                    <span className='md:ml-5'>MEME IT SO</span>
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
                <Route path="/search/:query" component={Search} />
                <Route path="/scene/ep/:ep/:ms" component={Scene} />
                <Route path="/meme/ep/:ep/:frame/t/:txt" component={Meme} />
            </Switch>
        </div>
    )
}

export default App;
