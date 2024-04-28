import axios from "axios";
// npm install axios

const api = axios.create({
  baseURL: "https://vacationhub.live", 
  // baseURL: "http://localhost:8080",
});

export default api;
