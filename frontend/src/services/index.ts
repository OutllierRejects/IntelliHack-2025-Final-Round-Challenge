// Service functions for API calls
import { api, endpoints } from "./api";
import type {
  HelpRequest,
  Task,
  Resource,
  User,
  Notification,
  DashboardStats,
  CreateRequestForm,
  UpdateTaskForm,
  CreateResourceForm,
  FilterOptions,
  PaginatedResponse,
  LoginForm,
  RegisterForm,
  AuthUser,
} from "../types";

// Authentication Services
export const authService = {
  login: async (
    credentials: LoginForm
  ): Promise<{ user: AuthUser; token: string }> => {
    return api.post(endpoints.auth.login, credentials);
  },

  register: async (
    userData: RegisterForm
  ): Promise<{ user: AuthUser; token: string }> => {
    return api.post(endpoints.auth.register, userData);
  },

  logout: async (): Promise<void> => {
    await api.post(endpoints.auth.logout);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },

  getProfile: async (): Promise<AuthUser> => {
    return api.get(endpoints.auth.profile);
  },

  updateProfile: async (updates: Partial<AuthUser>): Promise<AuthUser> => {
    return api.patch(endpoints.auth.profile, updates);
  },
};

// Request Services
export const requestService = {
  getRequests: async (
    filters?: FilterOptions
  ): Promise<PaginatedResponse<HelpRequest>> => {
    return api.get(endpoints.requests.list, filters);
  },

  getRequest: async (id: string): Promise<HelpRequest> => {
    return api.get(endpoints.requests.get(id));
  },

  createRequest: async (data: CreateRequestForm): Promise<HelpRequest> => {
    return api.post(endpoints.requests.create, data);
  },

  updateRequest: async (
    id: string,
    updates: Partial<HelpRequest>
  ): Promise<HelpRequest> => {
    return api.patch(endpoints.requests.update(id), updates);
  },

  deleteRequest: async (id: string): Promise<void> => {
    return api.delete(endpoints.requests.delete(id));
  },

  getMyRequests: async (): Promise<HelpRequest[]> => {
    return api.get(endpoints.requests.byUser);
  },

  getRequestStats: async (): Promise<any> => {
    return api.get(endpoints.requests.stats);
  },

  getDashboardData: async (): Promise<DashboardStats> => {
    return api.get(endpoints.requests.dashboard);
  },
};

// Task Services
export const taskService = {
  getTasks: async (
    filters?: FilterOptions
  ): Promise<PaginatedResponse<Task>> => {
    return api.get(endpoints.tasks.list, filters);
  },

  getTask: async (id: string): Promise<Task> => {
    return api.get(endpoints.tasks.get(id));
  },

  createTask: async (data: Partial<Task>): Promise<Task> => {
    return api.post(endpoints.tasks.create, data);
  },

  updateTask: async (id: string, updates: UpdateTaskForm): Promise<Task> => {
    return api.patch(endpoints.tasks.update(id), updates);
  },

  deleteTask: async (id: string): Promise<void> => {
    return api.delete(endpoints.tasks.delete(id));
  },

  assignTask: async (id: string, userId: string): Promise<Task> => {
    return api.post(endpoints.tasks.assign(id), { assigned_to: userId });
  },

  completeTask: async (id: string, notes?: string): Promise<Task> => {
    return api.post(endpoints.tasks.complete(id), { completion_notes: notes });
  },

  getMyTasks: async (): Promise<Task[]> => {
    return api.get(endpoints.tasks.myTasks);
  },

  getAvailableTasks: async (): Promise<Task[]> => {
    return api.get(endpoints.tasks.available);
  },
};

// Resource Services
export const resourceService = {
  getResources: async (
    filters?: FilterOptions
  ): Promise<PaginatedResponse<Resource>> => {
    return api.get(endpoints.resources.list, filters);
  },

  getResource: async (id: string): Promise<Resource> => {
    return api.get(endpoints.resources.get(id));
  },

  createResource: async (data: CreateResourceForm): Promise<Resource> => {
    return api.post(endpoints.resources.create, data);
  },

  updateResource: async (
    id: string,
    updates: Partial<Resource>
  ): Promise<Resource> => {
    return api.patch(endpoints.resources.update(id), updates);
  },

  deleteResource: async (id: string): Promise<void> => {
    return api.delete(endpoints.resources.delete(id));
  },

  consumeResource: async (data: {
    resource_id: string;
    quantity_used: number;
    task_id?: string;
    purpose?: string;
    notes?: string;
  }): Promise<void> => {
    return api.post(endpoints.resources.consume, data);
  },

  getLowStockResources: async (): Promise<Resource[]> => {
    return api.get(endpoints.resources.lowStock);
  },

  getResourceStats: async (): Promise<any> => {
    return api.get(endpoints.resources.stats);
  },
};

// User Services
export const userService = {
  getUsers: async (
    filters?: FilterOptions
  ): Promise<PaginatedResponse<User>> => {
    return api.get(endpoints.users.list, filters);
  },

  getUser: async (id: string): Promise<User> => {
    return api.get(endpoints.users.get(id));
  },

  updateUser: async (id: string, updates: Partial<User>): Promise<User> => {
    return api.patch(endpoints.users.update(id), updates);
  },

  getVolunteers: async (): Promise<User[]> => {
    return api.get(endpoints.users.volunteers);
  },

  getResponders: async (): Promise<User[]> => {
    return api.get(endpoints.users.responders);
  },

  updateAvailability: async (available: boolean): Promise<User> => {
    return api.patch(endpoints.users.profile, {
      availability_status: available,
    });
  },
};

// Notification Services
export const notificationService = {
  getNotifications: async (): Promise<Notification[]> => {
    return api.get(endpoints.notifications.list);
  },

  markAsRead: async (id: string): Promise<void> => {
    return api.post(endpoints.notifications.markRead(id));
  },

  markAllAsRead: async (): Promise<void> => {
    return api.post(endpoints.notifications.markAllRead);
  },

  getUnreadCount: async (): Promise<{ count: number }> => {
    return api.get(endpoints.notifications.unreadCount);
  },
};

// Dashboard Services
export const dashboardService = {
  getStats: async (): Promise<DashboardStats> => {
    return api.get(endpoints.dashboard.stats);
  },

  getOverview: async (): Promise<any> => {
    return api.get(endpoints.dashboard.overview);
  },

  getChartData: async (): Promise<any> => {
    return api.get(endpoints.dashboard.charts);
  },
};

// Agent Services
export const agentService = {
  getStatus: async (): Promise<any> => {
    return api.get(endpoints.agents.status);
  },

  getLogs: async (): Promise<any> => {
    return api.get(endpoints.agents.logs);
  },

  restart: async (): Promise<void> => {
    return api.post(endpoints.agents.restart);
  },
};

// WebSocket Service
export class WebSocketService {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectInterval: number = 5000;
  private maxReconnectAttempts: number = 5;
  private reconnectAttempts: number = 0;

  constructor(url: string = "ws://localhost:8000/ws") {
    this.url = url;
  }

  connect(onMessage?: (data: any) => void): void {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log("WebSocket connected");
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (onMessage) {
            onMessage(data);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket disconnected");
        this.attemptReconnect(onMessage);
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    } catch (error) {
      console.error("Failed to connect WebSocket:", error);
    }
  }

  private attemptReconnect(onMessage?: (data: any) => void): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`
      );

      setTimeout(() => {
        this.connect(onMessage);
      }, this.reconnectInterval);
    } else {
      console.error("Max reconnection attempts reached");
    }
  }

  send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.error("WebSocket is not connected");
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsService = new WebSocketService();
