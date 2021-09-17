export const anyErrorInterceptor = (error) => {
  if (error.response === undefined) return
  if (error.response.status >= 500) {
    error.message = `Internal error occured. Message from responce:\n${error.toJSON().message}`
    return Promise.reject(error);
  }
  if (error.response.status === 400) {
    error.message = `Bad request. Responce info:\n${error.response.data}`
    return Promise.reject(error);
  }
}

export const unknownErrorInterceptor = (error) => {
  if (error.response.status !== 200) {
    error.message = `Unknown error occured with status: ${error.response.status}`
    return Promise.reject(error);
  }
  
  if (error.response === undefined) {
    error.message = `Unknown error occured with status: ${error.response.status}`
    return Promise.reject(error);
  }
}

