import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // Update with actual backend URL
});

// Add token automatically if saved
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('auth_token');
  if (token && config.headers) {
    config.headers.Authorization = `JWT ${token}`;
  }
  return config;
});

export default api;
