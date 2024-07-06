// src/apiConfig.js
const getApiUrl = () => {
    return process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";
  };
  
  export default getApiUrl;
  