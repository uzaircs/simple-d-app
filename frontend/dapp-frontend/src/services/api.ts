import axios from 'axios';

const api = axios.create({
    baseURL: 'https://api.uzairkhan.me', // Replace with your API's base URL
    headers: {
      'Content-Type': 'application/json',
    },
    // You can add interceptors here for auth tokens or error handling if needed
  });
  
  export default api;