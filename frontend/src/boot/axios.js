
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default ({ app }) => {
  app.config.globalProperties.$api = api
  app.provide('api', api)
}

export { api }
