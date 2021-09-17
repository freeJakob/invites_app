import axios from 'axios'
import {
  anyErrorInterceptor,
  unknownErrorInterceptor,
} from '../requestInterceptors.js'


const apiEndpoint = 'api';

const _api = axios.create({
  baseURL: `/${apiEndpoint}/`,
  headers: {
    'Content-Type': 'application/json',
  },
});

_api.interceptors.response.use((response) => response, (error) => {
  anyErrorInterceptor(error);
  unknownErrorInterceptor(error);

  return Promise.reject(error);
});

export default _api;