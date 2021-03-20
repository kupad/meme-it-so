import React, { useState, useEffect } from 'react';

import search from './api.js';
import SearchResults from './SearchResults.js';

const Search = ({match: {params : {query}}}) => {
    const [ searching, setSearching ] = useState(true);
    const [ searchResults, setSearchResults] = useState([]);

    //anytime query changes, we get the data and and update the results
    useEffect(() => {
        if(!query) {
            setSearching(false);
            setSearchResults([]);
            return;
        }

        setSearching(true);
        setSearchResults([]);
        search(query).then(results => {
            //console.log(results);
            setSearchResults(results);
            setSearching(false)
        });
    }, [query]);

    return (
        <>
        {
            searching &&
            <div className='blink text-center text-6xl mt-10'>STAND BY</div>
        }
        <SearchResults results={searchResults} />
        </>
    );
};

export default Search;
