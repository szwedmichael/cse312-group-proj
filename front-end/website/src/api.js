import axios from "axios";
// npm install axios

const api = axios.create({
  baseURL: "https://vacationhub.live", // URL of the Fast API
});

export default api;
