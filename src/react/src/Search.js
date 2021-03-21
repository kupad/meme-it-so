import React, { useState, useEffect } from 'react';

import api from './api.js';
import StandBy from './lcars/StandBy.js'
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
        api.searchByQuery(query).then(results => {
            setSearchResults(results);
            setSearching(false)
        });
    }, [query]);

    const handleClick = (scene) => {
        console.log('ep', scene.ep, 'ms', scene.ms)
    }

    return (
        <div className="w-11/12 mx-auto mt-10">
            { searching && <StandBy /> }
            <SearchResults
                results={searchResults}
                onClick={handleClick}
            />
        </div>
    );
};

export default Search;
