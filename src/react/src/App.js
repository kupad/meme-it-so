import React, { useState } from 'react';

import { Switch, Route, useHistory } from "react-router-dom";

import LCARSBar from './lcars/LCARSBar.js'
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
            <header className='flex h-24 justify-center items-center'>
                <form className="w-5/12" onSubmit={handleSearch}>
                    <label className='hidden' htmlFor='search'>Search: </label>
                    <input
                        className='border-2 rounded-lg border-blue-600 text-3xl w-7/12 text-white bg-blue-900 bg-opacity-50 '
                        placeholder="search by quote"
                        type='text'
                        id='search'
                        value={searchTerm}
                        onChange={handleSearchChanged}
                    />
                <button className='bg-yellow-400 rounded-full font-bold text-black text-2xl pl-20 pt-1 pb-1 pr-4 ml-5' type='submit'>QUERY</button>
                </form>
            </header>
            <div className="w-99 mb-10 mx-auto">
                <LCARSBar msg="MEME IT SO"/>
            </div>
            <Switch>
                <Route path="/" exact render={() => <p></p>} />
                <Route path="/search/:query" component={Search} />
                <Route path="/scene/ep/:ep/:ms" component={Scene} />
                <Route path="/meme/ep/:ep/:frame/t/:txt" component={Meme} />
            </Switch>
        </div>
    )
}

export default App;
