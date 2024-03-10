import axios from 'axios';
// npm install axios

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // URL of the Fast API
});

export default api;