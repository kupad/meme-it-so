import React, { useState, useEffect } from 'react';
import search from './api.js';
import LCARSBar from './lcars/LCARSBar.js'
import SearchResults from './SearchResults.js'

function App() {
    const [ searching, setSearching ] = useState(false);
    const [ searchTerm, setSearchTerm ] = useState('');
    const [ searchResults, setSearchResults] = useState([]);

    const handleSearchChanged = (event) => {
        setSearchTerm(event.target.value)
        console.log(searchTerm)
    }

    const handleSearch = (event) => {
        setSearchResults([])
        setSearching(true)
        search(searchTerm).then(results => {
            //console.log(results);
            setSearchResults(results);
            setSearching(false)
        })
        event.preventDefault();
    };

    const season = (ep) => {
        return ep.substring(0,3);
    }

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
                {
                    searching &&
                    <div className='blink text-center text-6xl mt-10'>STAND BY</div>
                }
                <SearchResults results={searchResults} />
            </div>
        </div>
    )
}

export default App;
