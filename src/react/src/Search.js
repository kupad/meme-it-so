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

import { useState, useEffect } from 'react';

import api from './api.js';
import StandBy from './lcars/StandBy.js'
import SearchResults from './SearchResults.js';

const initialResults = {
    query: '',      //results for this query"
    page: 0,        //currently up to this page
    pageCount: 0,   //total pages
    hits: [],
    isLoading: false,
}

const Search = ({match: {params: {query: pquery}}}) => {

    const [ results, setResults] = useState(initialResults);
    const [ trigger, setTrigger ] = useState({
        query: pquery,
        page: 1
    });

    //when the query param changes, we need to:
    //  1) reset the results
    //  2) set the trigger to the new pquery, and set the page to 1
    if(pquery !== trigger.query) {
        setResults(initialResults)
        setTrigger({
            query: pquery,
            page: 1,
        })
    }

    useEffect(() => {
        //console.log('trigger', trigger)

        setResults(r => ({
            ...r,
            isLoading: true,
        }));
        api.searchByQuery(trigger.query, trigger.page).then(resp => {
            setResults(r => {
                //this guard is mostly here for development rerenders
                const same = trigger.query === r.query && trigger.page === r.page;
                return {
                    ...r,
                    page: resp.page,
                    pageCount: resp.pageCount,
                    hits: same ? r.hits : [...r.hits, ...resp.hits],
                    query: trigger.query,
                    isLoading: false,
                }
            })
        });
    }, [trigger]);

    const handleMore = () => setTrigger(t => ({
        ...t,
        page: t.page + 1
    }))

    return (
        <div className="w-11/12 mx-auto mt-10">
            { results.isLoading && <StandBy /> }
            <SearchResults
                results={results.hits}
                hasMore={results.page < results.pageCount}
                onMore={handleMore}
            />
        </div>
    );
};

export default Search;
