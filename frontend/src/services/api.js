/**
 * API service for communicating with the backend.
 */
import axios from 'axios';

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
      config.headers.Authorization = `Bearer ${window.Telegram.WebApp.initData}`;
    }
    return config;
  },
  (error) => {
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
