import React, { useState, useEffect } from 'react';
import search from './api.js';
import LCARSBar from './lcars/LCARSBar.js'

function App() {
    const [ searchTerm, setSearchTerm ] = useState('');
    const [ searchResults, setSearchResults] = useState([]);

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
        <div className='min-h-screen bg-gray-900 text-white'>
            <div className='container mx-auto'>
                <header className='flex h-24 justify-center items-center'>
                    <form className="w-5/12" onSubmit={handleSearch}>
                        <label className='hidden' htmlFor='search'>Search: </label>
                        <input
                            className='border-2 rounded-lg border-blue-600 text-3xl w-7/12 text-white bg-blue-900 bg-opacity-50 '
                            type='text'
                            id='search'
                            value={searchTerm}
                            onChange={handleSearchChanged}
                        />
                    <button className='bg-yellow-400 rounded-full font-bold text-black pl-20 pt-4 pb-1 pr-4 ml-5' type='submit'>SEARCH</button>
                    </form>
                </header>
                <LCARSBar msg="MEME IT SO"/>
                    <div className='w-11/12 mx-auto mt-5 flex flex-wrap'>
                        {
                            searchResults.map(scene => (
                                <div key={`${scene.ep}-${scene.srtidx}`} className='p-2'>
                                    <img src={scene.img} title={scene.content} width="320" height="240 "/>
                                </div>
                            ))
                        }
                    </div>
            </div>
        </div>
    )
}

export default App;
