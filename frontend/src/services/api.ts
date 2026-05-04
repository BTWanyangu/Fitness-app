import axios from 'axios';

export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export const MEDIA_BASE = import.meta.env.VITE_MEDIA_URL || 'http://localhost:8000';

export const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('trainova_access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
