/**
 * API service for communicating with the backend.
 */
import axios from 'axios';

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Log API configuration for debugging
console.log('[API Service] Initializing with URL:', API_URL);
console.log('[API Service] Environment:', import.meta.env.MODE);
console.log('[API Service] VITE_API_URL:', import.meta.env.VITE_API_URL);

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include Telegram initData
api.interceptors.request.use(
  (config) => {
    // Get initData from Telegram Web App
    if (window.Telegram?.WebApp?.initData) {
      // Send initData directly in Authorization header without "Bearer " prefix
      config.headers.Authorization = window.Telegram.WebApp.initData;
      console.log('[API Service] Request with initData:', config.method.toUpperCase(), config.url);
    } else {
      console.warn('[API Service] ⚠️ Missing Telegram initData! Request may fail with 401.');
      console.warn('[API Service] Make sure you are opening the app from Telegram.');
    }
    return config;
  },
  (error) => {
    console.error('[API Service] Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('[API Service] ✓ Success:', response.config.method.toUpperCase(), response.config.url, response.status);
    return response;
  },
  (error) => {
    // Log detailed error information
    if (error.response) {
      // Server responded with error status
      console.error('[API Service] ✗ Server Error:', {
        status: error.response.status,
        statusText: error.response.statusText,
        url: error.config?.url,
        method: error.config?.method?.toUpperCase(),
        data: error.response.data
      });
      
      if (error.response.status === 401) {
        console.error('[API Service] 401 Unauthorized - Possible reasons:');
        console.error('  1. Missing or invalid Telegram initData');
        console.error('  2. App not opened from Telegram');
        console.error('  3. Frontend connecting to wrong API URL');
        console.error('  Current API URL:', API_URL);
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('[API Service] ✗ Network Error: No response received');
      console.error('  URL:', error.config?.url);
      console.error('  Possible reasons:');
      console.error('    1. API server is down');
      console.error('    2. CORS issues');
      console.error('    3. Wrong API URL configured');
      console.error('    Current API URL:', API_URL);
    } else {
      // Error setting up request
      console.error('[API Service] ✗ Request Setup Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API methods
export const tasksAPI = {
  /**
   * Get all tasks
   * @param {Object} filters - Optional filters (status, priority)
   * @returns {Promise} List of tasks
   */
  getTasks: (filters = {}) => {
    return api.get('/api/tasks', { params: filters });
  },

  /**
   * Create a new task
   * @param {Object} taskData - Task data
   * @returns {Promise} Created task
   */
  createTask: (taskData) => {
    return api.post('/api/tasks', taskData);
  },

  /**
   * Update a task
   * @param {number} taskId - Task ID
   * @param {Object} taskData - Updated task data
   * @returns {Promise} Updated task
   */
  updateTask: (taskId, taskData) => {
    return api.put(`/api/tasks/${taskId}`, taskData);
  },

  /**
   * Delete a task
   * @param {number} taskId - Task ID
   * @returns {Promise} Deletion result
   */
  deleteTask: (taskId) => {
    return api.delete(`/api/tasks/${taskId}`);
  },

  /**
   * Get task statistics
   * @returns {Promise} Task statistics
   */
  getStats: () => {
    return api.get('/api/tasks/stats');
  },
};

export default api;
