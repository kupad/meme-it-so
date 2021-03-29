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
