import _api from './index.js';

export const fetchCheckedInUsers = (_store, queryParameters) => {
  return _api.get(`users/list_arrived/`, {
    params: queryParameters,
  })
    .then(response => {
      return response.data
    })
}
