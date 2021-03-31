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
import { Link } from "react-router-dom";

import Button from './lcars/Button.js'

const SearchResults = ({results, hasMore, onMore}) => {
    const key = (scene) => {
        return `${scene.ep}-${scene.srtidx}`;
    }

    return (
        <div>
            <div className='flex flex-wrap'>
            {
                results.map(scene => (
                    <Link
                        key={key(scene)}
                        to={`/scene/ep/${scene.ep}/${scene.start}`}
                        className='p-2'
                    >
                        <img src={scene.img_url} title={scene.content} alt={key(scene)} width="320" height="240" />
                    </Link>
                ))
            }
            </div>
            <div className='text-center my-2'>
            {
                hasMore &&
                <Button onClick={onMore}>MORE</Button>
            }
            </div>
        </div>
    );
};

export default SearchResults;
