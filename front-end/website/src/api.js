import axios from 'axios';
// npm install axios

const api = axios.create({
    baseURL: 'http://localhost:8000', // URL of the Fast API
});

export default api;