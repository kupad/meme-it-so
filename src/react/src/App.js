import React, { useState, useEffect } from 'react';
import search from './api.js';
import './App.css';

function App() {
    const [ searchTerm, setSearchTerm ] = useState('');
    const [ searchResults, setSearchResults] = useState([]);

    useEffect(() =>{
        /*
        fetch('/search/?q=prune').then(res => res.json())
            .then(data => {
                setSearchResults(data.matches)
            });
        */
    }, []);

    const handleSearchChanged = (event) => {
        setSearchTerm(event.target.value)
        console.log(searchTerm)
    }

    const handleSearch = (event) => {
        search(searchTerm).then(results => {
            console.log(results);
            setSearchResults(results);
        })
        event.preventDefault();
    };

    const season = (ep) => {
        return ep.substring(0,3);
    }

    return (
        <div id="all">
            <header className="header">
                <div className="lcars-left-bar-top lcars-bg-purple lcars-w-200" />
                    <div className="bd-5-green flex-col flex-grow flex-just-right">
                        <div id="meme-it-so">Meme It So</div>
                        <form className="bd-5-green" onSubmit={handleSearch}>
                            <label htmlFor='search'>Search: </label>
                            <input
                                type='text'
                                id='search'
                                value={searchTerm}
                                onChange={handleSearchChanged}
                            />
                            <button type='submit'>Make It So</button>
                        </form>
                        <div className='lcars-flex-grow' />
                        <div className="lcars-bar">
                            <div className="lcars-bg-purple lcars-w-400" />
                            <div className="lcars-bg-purple lcars-w-40" />
                            <div className="lcars-bg-purple lcars-w-200" />
                            <div className="lcars-bg-purple lcars-flex-grow" />
                            <div className="lcars-bg-purple lcars-w-50" />
                        </div>
                    </div>
            </header>
            <div className="content">
                <div className='searchResults'>
                    {
                        searchResults.map(scene => (
                            <div className='result' key={`${scene.ep}-${scene.srtidx}`}>
                                <img src={scene.img} title={scene.content} />
                            </div>
                        ))
                    }
                </div>
            </div>
        </div>
  );
}

export default App;
