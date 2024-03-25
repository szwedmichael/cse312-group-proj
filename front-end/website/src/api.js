import axios from "axios";
// npm install axios

const api = axios.create({
  baseURL: "http://0.0.0.0:8080", // URL of the Fast API
});

export default api;
