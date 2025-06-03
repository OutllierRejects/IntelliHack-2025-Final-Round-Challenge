// API configuration and base client
import axios, { AxiosInstance, AxiosResponse } from "axios";
import type { ApiResponse, PaginatedResponse } from "../types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Generic API functions
export const api = {
  get: async <T>(url: string, params?: any): Promise<T> => {
    const response = await apiClient.get(url, { params });
    return response.data;
  },

  post: async <T>(url: string, data?: any): Promise<T> => {
    const response = await apiClient.post(url, data);
    return response.data;
  },

  put: async <T>(url: string, data?: any): Promise<T> => {
    const response = await apiClient.put(url, data);
    return response.data;
  },

  patch: async <T>(url: string, data?: any): Promise<T> => {
    const response = await apiClient.patch(url, data);
    return response.data;
  },

  delete: async <T>(url: string): Promise<T> => {
    const response = await apiClient.delete(url);
    return response.data;
  },
};

// API endpoints
export const endpoints = {
  // Authentication
  auth: {
    login: "/auth/login",
    register: "/auth/register",
    logout: "/auth/logout",
    refresh: "/auth/refresh",
    profile: "/auth/profile",
  },

  // Help requests
  requests: {
    list: "/requests",
    create: "/requests",
    get: (id: string) => `/requests/${id}`,
    update: (id: string) => `/requests/${id}`,
    delete: (id: string) => `/requests/${id}`,
    stats: "/requests/stats",
    dashboard: "/requests/dashboard",
    byUser: "/requests/my",
  },

  // Tasks
  tasks: {
    list: "/tasks",
    create: "/tasks",
    get: (id: string) => `/tasks/${id}`,
    update: (id: string) => `/tasks/${id}`,
    delete: (id: string) => `/tasks/${id}`,
    assign: (id: string) => `/tasks/${id}/assign`,
    complete: (id: string) => `/tasks/${id}/complete`,
    myTasks: "/tasks/my",
    available: "/tasks/available",
  },

  // Resources
  resources: {
    list: "/resources",
    create: "/resources",
    get: (id: string) => `/resources/${id}`,
    update: (id: string) => `/resources/${id}`,
    delete: (id: string) => `/resources/${id}`,
    consume: "/resources/consume",
    lowStock: "/resources/low-stock",
    stats: "/resources/stats",
  },

  // Users
  users: {
    list: "/users",
    get: (id: string) => `/users/${id}`,
    update: (id: string) => `/users/${id}`,
    profile: "/users/profile",
    volunteers: "/users/volunteers",
    responders: "/users/responders",
  },

  // Notifications
  notifications: {
    list: "/notifications",
    markRead: (id: string) => `/notifications/${id}/read`,
    markAllRead: "/notifications/mark-all-read",
    unreadCount: "/notifications/unread-count",
  },

  // Dashboard
  dashboard: {
    stats: "/dashboard/stats",
    overview: "/dashboard/overview",
    charts: "/dashboard/charts",
  },

  // Agents
  agents: {
    status: "/agents/status",
    logs: "/agents/logs",
    restart: "/agents/restart",
  },
};

export default apiClient;
