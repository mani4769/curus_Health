import axios from 'axios';
import { LoginData, SignupData, AuthResponse } from '../types';

// For production deployment, point to your Render backend
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (data: LoginData): Promise<AuthResponse> => {
    console.log('📡 Making login request to:', `${API_BASE_URL}/api/auth/login`, 'with data:', data);
    return api.post('/api/auth/login', data).then(res => {
      console.log('📡 Login response:', res.data);
      return res.data;
    });
  },
  
  signup: (data: SignupData) =>
    api.post('/api/auth/signup', data).then(res => res.data),
};

export const userAPI = {
  getUsers: () => api.get('/api/users').then(res => res.data),
  getProfile: () => api.get('/api/users/profile').then(res => res.data),
  updateUser: (id: string, data: any) => 
    api.put(`/api/users/${id}`, data).then(res => res.data),
  deleteUser: (id: string) => 
    api.delete(`/api/users/${id}`).then(res => res.data),
};

export const projectAPI = {
  getProjects: () => api.get('/api/projects').then(res => res.data),
  getProject: (id: string) => api.get(`/api/projects/${id}`).then(res => res.data),
  createProject: (data: any) => api.post('/api/projects', data).then(res => res.data),
  updateProject: (id: string, data: any) => 
    api.put(`/api/projects/${id}`, data).then(res => res.data),
  deleteProject: (id: string) => 
    api.delete(`/api/projects/${id}`).then(res => res.data),
  addTeamMember: (projectId: string, userId: string) =>
    api.post(`/api/projects/${projectId}/team`, { user_id: userId }).then(res => res.data),
  removeTeamMember: (projectId: string, userId: string) =>
    api.delete(`/api/projects/${projectId}/team/${userId}`).then(res => res.data),
};

export const taskAPI = {
  getTasks: (params?: any) => {
    const queryString = params ? `?${new URLSearchParams(params).toString()}` : '';
    return api.get(`/api/tasks${queryString}`).then(res => res.data);
  },
  getTask: (id: string) => api.get(`/api/tasks/${id}`).then(res => res.data),
  createTask: (data: any) => api.post('/api/tasks', data).then(res => res.data),
  updateTask: (id: string, data: any) => 
    api.put(`/api/tasks/${id}`, data).then(res => res.data),
  updateTaskStatus: (id: string, status: string) =>
    api.patch(`/api/tasks/${id}/status`, { status }).then(res => res.data),
  addComment: (id: string, comment: string) =>
    api.post(`/api/tasks/${id}/comments`, { comment }).then(res => res.data),
  deleteTask: (id: string) => 
    api.delete(`/api/tasks/${id}`).then(res => res.data),
};

export const reportAPI = {
  getTasksByStatus: () => api.get('/api/reports/tasks-by-status').then(res => res.data),
  getOverdueTasks: () => api.get('/api/reports/overdue-tasks').then(res => res.data),
  getDashboard: () => api.get('/api/reports/dashboard').then(res => res.data),
  getUserWorkload: () => api.get('/api/reports/user-workload').then(res => res.data),
};

export default api;
