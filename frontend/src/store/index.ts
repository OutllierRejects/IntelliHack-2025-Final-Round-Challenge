// Zustand store for global state management
import { create } from "zustand";
import { devtools } from "zustand/middleware";
import type {
  AuthUser,
  HelpRequest,
  Task,
  Resource,
  Notification,
  DashboardStats,
} from "../types";

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (user: AuthUser) => void;
  logout: () => void;
  updateUser: (updates: Partial<AuthUser>) => void;
  setLoading: (loading: boolean) => void;
  initializeAuth: () => void;
}

interface RequestState {
  requests: HelpRequest[];
  selectedRequest: HelpRequest | null;
  isLoading: boolean;
  filters: {
    status?: string[];
    priority?: string[];
    search?: string;
  };
  setRequests: (requests: HelpRequest[]) => void;
  addRequest: (request: HelpRequest) => void;
  updateRequest: (id: string, updates: Partial<HelpRequest>) => void;
  setSelectedRequest: (request: HelpRequest | null) => void;
  setLoading: (loading: boolean) => void;
  setFilters: (filters: any) => void;
}

interface TaskState {
  tasks: Task[];
  myTasks: Task[];
  selectedTask: Task | null;
  isLoading: boolean;
  setTasks: (tasks: Task[]) => void;
  setMyTasks: (tasks: Task[]) => void;
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  setSelectedTask: (task: Task | null) => void;
  setLoading: (loading: boolean) => void;
}

interface ResourceState {
  resources: Resource[];
  lowStockResources: Resource[];
  isLoading: boolean;
  setResources: (resources: Resource[]) => void;
  addResource: (resource: Resource) => void;
  updateResource: (id: string, updates: Partial<Resource>) => void;
  setLowStockResources: (resources: Resource[]) => void;
  setLoading: (loading: boolean) => void;
}

interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  isLoading: boolean;
  setNotifications: (notifications: Notification[]) => void;
  addNotification: (notification: Notification) => void;
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  setLoading: (loading: boolean) => void;
}

interface DashboardState {
  stats: DashboardStats | null;
  isLoading: boolean;
  lastUpdated: string | null;
  setStats: (stats: DashboardStats) => void;
  setLoading: (loading: boolean) => void;
  setLastUpdated: (timestamp: string) => void;
}

interface UIState {
  sidebarOpen: boolean;
  theme: "light" | "dark";
  activeTab: string;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setTheme: (theme: "light" | "dark") => void;
  setActiveTab: (tab: string) => void;
}

// Auth Store
export const useAuthStore = create<AuthState>()(
  devtools(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: (user) =>
        set({ user, isAuthenticated: true }, false, "auth/login"),
      logout: () =>
        set({ user: null, isAuthenticated: false }, false, "auth/logout"),
      updateUser: (updates) =>
        set(
          (state) => ({
            user: state.user ? { ...state.user, ...updates } : null,
          }),
          false,
          "auth/updateUser"
        ),
      setLoading: (isLoading) => set({ isLoading }, false, "auth/setLoading"),
      initializeAuth: () => {
        // Check if there's a stored token or session
        const token = localStorage.getItem("auth_token");
        const user = localStorage.getItem("auth_user");
        if (token && user) {
          try {
            const parsedUser = JSON.parse(user);
            set(
              { user: parsedUser, isAuthenticated: true },
              false,
              "auth/initializeAuth"
            );
          } catch {
            // Clear invalid data
            localStorage.removeItem("auth_token");
            localStorage.removeItem("auth_user");
          }
        }
      },
    }),
    { name: "auth-store" }
  )
);

// Request Store
export const useRequestStore = create<RequestState>()(
  devtools(
    (set) => ({
      requests: [],
      selectedRequest: null,
      isLoading: false,
      filters: {},
      setRequests: (requests) =>
        set({ requests }, false, "requests/setRequests"),
      addRequest: (request) =>
        set(
          (state) => ({
            requests: [request, ...state.requests],
          }),
          false,
          "requests/addRequest"
        ),
      updateRequest: (id, updates) =>
        set(
          (state) => ({
            requests: state.requests.map((req) =>
              req.id === id ? { ...req, ...updates } : req
            ),
            selectedRequest:
              state.selectedRequest?.id === id
                ? { ...state.selectedRequest, ...updates }
                : state.selectedRequest,
          }),
          false,
          "requests/updateRequest"
        ),
      setSelectedRequest: (request) =>
        set({ selectedRequest: request }, false, "requests/setSelectedRequest"),
      setLoading: (isLoading) =>
        set({ isLoading }, false, "requests/setLoading"),
      setFilters: (filters) => set({ filters }, false, "requests/setFilters"),
    }),
    { name: "request-store" }
  )
);

// Task Store
export const useTaskStore = create<TaskState>()(
  devtools(
    (set) => ({
      tasks: [],
      myTasks: [],
      selectedTask: null,
      isLoading: false,
      setTasks: (tasks) => set({ tasks }, false, "tasks/setTasks"),
      setMyTasks: (myTasks) => set({ myTasks }, false, "tasks/setMyTasks"),
      addTask: (task) =>
        set(
          (state) => ({
            tasks: [task, ...state.tasks],
          }),
          false,
          "tasks/addTask"
        ),
      updateTask: (id, updates) =>
        set(
          (state) => ({
            tasks: state.tasks.map((task) =>
              task.id === id ? { ...task, ...updates } : task
            ),
            myTasks: state.myTasks.map((task) =>
              task.id === id ? { ...task, ...updates } : task
            ),
            selectedTask:
              state.selectedTask?.id === id
                ? { ...state.selectedTask, ...updates }
                : state.selectedTask,
          }),
          false,
          "tasks/updateTask"
        ),
      setSelectedTask: (task) =>
        set({ selectedTask: task }, false, "tasks/setSelectedTask"),
      setLoading: (isLoading) => set({ isLoading }, false, "tasks/setLoading"),
    }),
    { name: "task-store" }
  )
);

// Resource Store
export const useResourceStore = create<ResourceState>()(
  devtools(
    (set) => ({
      resources: [],
      lowStockResources: [],
      isLoading: false,
      setResources: (resources) =>
        set({ resources }, false, "resources/setResources"),
      addResource: (resource) =>
        set(
          (state) => ({
            resources: [resource, ...state.resources],
          }),
          false,
          "resources/addResource"
        ),
      updateResource: (id, updates) =>
        set(
          (state) => ({
            resources: state.resources.map((resource) =>
              resource.id === id ? { ...resource, ...updates } : resource
            ),
          }),
          false,
          "resources/updateResource"
        ),
      setLowStockResources: (lowStockResources) =>
        set({ lowStockResources }, false, "resources/setLowStockResources"),
      setLoading: (isLoading) =>
        set({ isLoading }, false, "resources/setLoading"),
    }),
    { name: "resource-store" }
  )
);

// Notification Store
export const useNotificationStore = create<NotificationState>()(
  devtools(
    (set) => ({
      notifications: [],
      unreadCount: 0,
      isLoading: false,
      setNotifications: (notifications) =>
        set(
          {
            notifications,
            unreadCount: notifications.filter((n) => !n.is_read).length,
          },
          false,
          "notifications/setNotifications"
        ),
      addNotification: (notification) =>
        set(
          (state) => ({
            notifications: [notification, ...state.notifications],
            unreadCount: notification.is_read
              ? state.unreadCount
              : state.unreadCount + 1,
          }),
          false,
          "notifications/addNotification"
        ),
      markAsRead: (id) =>
        set(
          (state) => ({
            notifications: state.notifications.map((notification) =>
              notification.id === id
                ? { ...notification, is_read: true }
                : notification
            ),
            unreadCount: Math.max(0, state.unreadCount - 1),
          }),
          false,
          "notifications/markAsRead"
        ),
      markAllAsRead: () =>
        set(
          (state) => ({
            notifications: state.notifications.map((notification) => ({
              ...notification,
              is_read: true,
            })),
            unreadCount: 0,
          }),
          false,
          "notifications/markAllAsRead"
        ),
      setLoading: (isLoading) =>
        set({ isLoading }, false, "notifications/setLoading"),
    }),
    { name: "notification-store" }
  )
);

// Dashboard Store
export const useDashboardStore = create<DashboardState>()(
  devtools(
    (set) => ({
      stats: null,
      isLoading: false,
      lastUpdated: null,
      setStats: (stats) => set({ stats }, false, "dashboard/setStats"),
      setLoading: (isLoading) =>
        set({ isLoading }, false, "dashboard/setLoading"),
      setLastUpdated: (lastUpdated) =>
        set({ lastUpdated }, false, "dashboard/setLastUpdated"),
    }),
    { name: "dashboard-store" }
  )
);

// UI Store
export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      sidebarOpen: true,
      theme: "light",
      activeTab: "dashboard",
      setSidebarOpen: (sidebarOpen) =>
        set({ sidebarOpen }, false, "ui/setSidebarOpen"),
      toggleSidebar: () =>
        set(
          (state) => ({ sidebarOpen: !state.sidebarOpen }),
          false,
          "ui/toggleSidebar"
        ),
      setTheme: (theme) => set({ theme }, false, "ui/setTheme"),
      setActiveTab: (activeTab) => set({ activeTab }, false, "ui/setActiveTab"),
    }),
    { name: "ui-store" }
  )
);

// Combined hook for convenience
export const useStore = () => ({
  auth: useAuthStore(),
  requests: useRequestStore(),
  tasks: useTaskStore(),
  resources: useResourceStore(),
  notifications: useNotificationStore(),
  dashboard: useDashboardStore(),
  ui: useUIStore(),
});
