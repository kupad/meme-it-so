import axios from 'axios';

const API_ENDPOINT = "http://localhost:3000/api";

const search = async (query) => {
    try {
        const response = await axios.get(`${API_ENDPOINT}/search/?q=${query}`);
        //console.log(response);
        return response.data.matches;
    } catch(error) {
        console.log(error)
        return [];
    }
};

export default search;
