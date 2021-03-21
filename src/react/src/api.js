import axios from 'axios';

const API_ENDPOINT = "http://localhost:3000/api";

export const searchByQuery = async (query) => {
    try {
        const response = await axios.get(`${API_ENDPOINT}/search/?q=${query}`);
        //console.log(response);
        return response.data.matches;
    } catch(error) {
        console.log(error)
        return [];
    }
};

export const searchByTime = async (ep, ms) => {
    try {
        const response = await axios.get(`${API_ENDPOINT}/search/ep/${ep}/${ms}`);
        //console.log(response);
        return response.data;
    } catch(error) {
        console.log(error)
        return {};
    }
}

export default { searchByQuery, searchByTime };
