import React, { useState } from 'react';

import { Switch, Route, useHistory } from "react-router-dom";

import LCARSBar from './lcars/LCARSBar.js'
import Search from './Search.js'

function App() {
    const history = useHistory();
    console.log(history)

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
        <div className='min-h-screen bg-gray-800 text-white'>
            <div className='container mx-auto'>
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
                    <button className='bg-yellow-400 rounded-full font-bold text-black text-2xl pl-20 pt-1 pb-1 pr-4 ml-5' type='submit'>SEARCH</button>
                    </form>
                </header>
                <LCARSBar msg="MEME IT SO"/>
                <Switch>
                    <Route path="/" exact render={() => <p></p>} /> //TODO: have something here!
                    <Route path="/search/:query" component={Search} />
                </Switch>
            </div>
        </div>
    )
}

export default App;
