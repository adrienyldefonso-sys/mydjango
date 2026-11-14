import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/optica-v3/api',
  timeout: 10000,
})

export const apiOjoChakra = axios.create({
  baseURL: 'http://127.0.0.1:8001/api',
  timeout: 10000,
})

export default api
