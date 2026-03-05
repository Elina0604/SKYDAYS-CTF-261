import axios from 'axios'
import type { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// API Configuration with runtime detection
const getApiBaseUrl = (): string => {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
  }
  return `${window.location.protocol}//${window.location.host}/api`;
};

const API_BASE_URL = getApiBaseUrl();

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging (development)
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors and logging
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    if (import.meta.env.DEV) {
      console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    }
    return response
  },
  (error: AxiosError) => {
    const status = error.response?.status
    const message = (error.response?.data as any)?.detail || error.message
    const vaderQuote = (error.response?.data as any)?.vader_quote
    
    console.error(`❌ API Error [${status}]:`, message)
    
    if (vaderQuote) {
      console.log(`💬 Vader says: "${vaderQuote}"`)
    }
    
    // Enhance error with user-friendly message
    const enhancedError = {
      ...error,
      userMessage: message,
      vaderQuote: vaderQuote,
      isNetworkError: !error.response,
      isServerError: status && status >= 500,
      isClientError: status && status >= 400 && status < 500,
    }
    
    return Promise.reject(enhancedError)
  }
)

// API availability checker
let apiAvailable: boolean | null = null

export const checkApiAvailability = async (): Promise<boolean> => {
  try {
    await apiClient.get('/health')
    apiAvailable = true
    return true
  } catch (error) {
    apiAvailable = false
    console.warn('⚠️ API not available, falling back to localStorage')
    return false
  }
}

export const isApiAvailable = (): boolean => {
  return apiAvailable === true
}

export { apiClient }
export default apiClient