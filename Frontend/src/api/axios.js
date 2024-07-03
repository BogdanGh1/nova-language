import axios from 'axios';

export default axios.create({
    baseURL: 'http://3.76.122.165/',
    headers: { "ngrok-skip-browser-warning": "true" }
});