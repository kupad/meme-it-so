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

import axios from 'axios';

import {padFrame} from './utils.js'

const API_ENDPOINT = "http://localhost:3000/api";

class API {

    static async searchByQuery(query, page) {
        console.log('searchByQuery', 'query:', query,'page:',page)
        try {
            const response = await axios.get(`${API_ENDPOINT}/search/?q=${query}&page=${page}`);
            //console.log(response);
            return response.data;
        } catch(error) {
            console.log(error)
            return {'hits': [], 'page': 0, 'pagecount': 0};
        }
    };

    static async searchByTime(ep, ms) {
        try {
            const response = await axios.get(`${API_ENDPOINT}/search/ep/${ep}/${ms}`);
            //console.log(response);
            return response.data;
        } catch(error) {
            console.log(error)
            return {};
        }
    }

    static async getAllScenes(ep, page=1) {
        try {
            const response = await axios.get(`${API_ENDPOINT}/episode/${ep}?page=${page}`);
            //console.log(response);
            return response.data;
        } catch(error) {
            console.log(error)
            return {};
        }
    }

    static gifUrl(ep, startframe, endframe) {
        return `/api/gif/ep/${ep}/${padFrame(startframe)}.${padFrame(endframe)}.gif`
    }

    //get the gif as base64 encoded string
    static async genGif(ep, start, end) {
        try {
            const response = await axios.get(this.gifUrl(ep,start,end), { responseType: 'arraybuffer'});
            return Buffer.from(response.data, 'binary').toString('base64');
        } catch(error) {
            console.log(error)
        }
    }
}

export default API;
