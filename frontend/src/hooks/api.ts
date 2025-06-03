// Custom React hooks for API integration using React Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import {
  requestService,
  taskService,
  resourceService,
  userService,
  notificationService,
  dashboardService,
  authService,
} from '../services'
import type {
  HelpRequest,
  Task,
  Resource,
  FilterOptions,
  CreateRequestForm,
  UpdateTaskForm,
  CreateResourceForm,
  LoginForm,
  RegisterForm,
} from '../types'

// Query keys
export const queryKeys = {
  requests: ['requests'],
  request: (id: string) => ['requests', id],
  myRequests: ['requests', 'my'],
  
  tasks: ['tasks'],
  task: (id: string) => ['tasks', id],
  myTasks: ['tasks', 'my'],
  availableTasks: ['tasks', 'available'],
  
  resources: ['resources'],
  resource: (id: string) => ['resources', id],
  lowStockResources: ['resources', 'low-stock'],
  
  users: ['users'],
  user: (id: string) => ['users', id],
  volunteers: ['users', 'volunteers'],
  responders: ['users', 'responders'],
  
  notifications: ['notifications'],
  unreadCount: ['notifications', 'unread-count'],
  
  dashboard: ['dashboard'],
  dashboardStats: ['dashboard', 'stats'],
  
  profile: ['profile'],
}

// Request hooks
export const useRequests = (filters?: FilterOptions) => {
  return useQuery({
    queryKey: [...queryKeys.requests, filters],
    queryFn: () => requestService.getRequests(filters),
    staleTime: 30000, // 30 seconds
  })
}

export const useRequest = (id: string) => {
  return useQuery({
    queryKey: queryKeys.request(id),
    queryFn: () => requestService.getRequest(id),
    enabled: !!id,
  })
}

export const useMyRequests = () => {
  return useQuery({
    queryKey: queryKeys.myRequests,
    queryFn: () => requestService.getMyRequests(),
  })
}

export const useCreateRequest = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreateRequestForm) => requestService.createRequest(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.requests })
      queryClient.invalidateQueries({ queryKey: queryKeys.myRequests })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboardStats })
      toast.success('Help request submitted successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to submit request')
    },
  })
}

export const useUpdateRequest = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: Partial<HelpRequest> }) =>
      requestService.updateRequest(id, updates),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(queryKeys.request(variables.id), data)
      queryClient.invalidateQueries({ queryKey: queryKeys.requests })
      queryClient.invalidateQueries({ queryKey: queryKeys.myRequests })
      toast.success('Request updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update request')
    },
  })
}

// Task hooks
export const useTasks = (filters?: FilterOptions) => {
  return useQuery({
    queryKey: [...queryKeys.tasks, filters],
    queryFn: () => taskService.getTasks(filters),
    staleTime: 30000,
  })
}

export const useTask = (id: string) => {
  return useQuery({
    queryKey: queryKeys.task(id),
    queryFn: () => taskService.getTask(id),
    enabled: !!id,
  })
}

export const useMyTasks = () => {
  return useQuery({
    queryKey: queryKeys.myTasks,
    queryFn: () => taskService.getMyTasks(),
  })
}

export const useAvailableTasks = () => {
  return useQuery({
    queryKey: queryKeys.availableTasks,
    queryFn: () => taskService.getAvailableTasks(),
  })
}

export const useUpdateTask = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: UpdateTaskForm }) =>
      taskService.updateTask(id, updates),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(queryKeys.task(variables.id), data)
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks })
      queryClient.invalidateQueries({ queryKey: queryKeys.myTasks })
      toast.success('Task updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update task')
    },
  })
}

export const useAssignTask = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, userId }: { id: string; userId: string }) =>
      taskService.assignTask(id, userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks })
      queryClient.invalidateQueries({ queryKey: queryKeys.myTasks })
      queryClient.invalidateQueries({ queryKey: queryKeys.availableTasks })
      toast.success('Task assigned successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to assign task')
    },
  })
}

export const useCompleteTask = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, notes }: { id: string; notes?: string }) =>
      taskService.completeTask(id, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks })
      queryClient.invalidateQueries({ queryKey: queryKeys.myTasks })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboardStats })
      toast.success('Task completed successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to complete task')
    },
  })
}

// Resource hooks
export const useResources = (filters?: FilterOptions) => {
  return useQuery({
    queryKey: [...queryKeys.resources, filters],
    queryFn: () => resourceService.getResources(filters),
    staleTime: 60000, // 1 minute
  })
}

export const useResource = (id: string) => {
  return useQuery({
    queryKey: queryKeys.resource(id),
    queryFn: () => resourceService.getResource(id),
    enabled: !!id,
  })
}

export const useLowStockResources = () => {
  return useQuery({
    queryKey: queryKeys.lowStockResources,
    queryFn: () => resourceService.getLowStockResources(),
  })
}

export const useCreateResource = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreateResourceForm) => resourceService.createResource(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.resources })
      queryClient.invalidateQueries({ queryKey: queryKeys.lowStockResources })
      toast.success('Resource created successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create resource')
    },
  })
}

export const useUpdateResource = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: Partial<Resource> }) =>
      resourceService.updateResource(id, updates),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(queryKeys.resource(variables.id), data)
      queryClient.invalidateQueries({ queryKey: queryKeys.resources })
      queryClient.invalidateQueries({ queryKey: queryKeys.lowStockResources })
      toast.success('Resource updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update resource')
    },
  })
}

export const useConsumeResource = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: {
      resource_id: string
      quantity_used: number
      task_id?: string
      purpose?: string
      notes?: string
    }) => resourceService.consumeResource(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.resources })
      queryClient.invalidateQueries({ queryKey: queryKeys.lowStockResources })
      toast.success('Resource consumption recorded!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to record resource consumption')
    },
  })
}

// User hooks
export const useVolunteers = () => {
  return useQuery({
    queryKey: queryKeys.volunteers,
    queryFn: () => userService.getVolunteers(),
  })
}

export const useResponders = () => {
  return useQuery({
    queryKey: queryKeys.responders,
    queryFn: () => userService.getResponders(),
  })
}

export const useUpdateAvailability = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (available: boolean) => userService.updateAvailability(available),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.profile })
      queryClient.invalidateQueries({ queryKey: queryKeys.volunteers })
      queryClient.invalidateQueries({ queryKey: queryKeys.responders })
      toast.success('Availability updated!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update availability')
    },
  })
}

// Notification hooks
export const useNotifications = () => {
  return useQuery({
    queryKey: queryKeys.notifications,
    queryFn: () => notificationService.getNotifications(),
    refetchInterval: 30000, // Refetch every 30 seconds
  })
}

export const useUnreadCount = () => {
  return useQuery({
    queryKey: queryKeys.unreadCount,
    queryFn: () => notificationService.getUnreadCount(),
    refetchInterval: 15000, // Refetch every 15 seconds
  })
}

export const useMarkAsRead = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => notificationService.markAsRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.notifications })
      queryClient.invalidateQueries({ queryKey: queryKeys.unreadCount })
    },
  })
}

export const useMarkAllAsRead = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: () => notificationService.markAllAsRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.notifications })
      queryClient.invalidateQueries({ queryKey: queryKeys.unreadCount })
      toast.success('All notifications marked as read!')
    },
  })
}

// Dashboard hooks
export const useDashboardStats = () => {
  return useQuery({
    queryKey: queryKeys.dashboardStats,
    queryFn: () => dashboardService.getStats(),
    staleTime: 60000, // 1 minute
    refetchInterval: 120000, // Refetch every 2 minutes
  })
}

// Auth hooks
export const useLogin = () => {
  return useMutation({
    mutationFn: (credentials: LoginForm) => authService.login(credentials),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      toast.success('Login successful!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Login failed')
    },
  })
}

export const useRegister = () => {
  return useMutation({
    mutationFn: (userData: RegisterForm) => authService.register(userData),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      toast.success('Registration successful!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Registration failed')
    },
  })
}

export const useProfile = () => {
  return useQuery({
    queryKey: queryKeys.profile,
    queryFn: () => authService.getProfile(),
    staleTime: 300000, // 5 minutes
  })
}

export const useUpdateProfile = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (updates: Partial<any>) => authService.updateProfile(updates),
    onSuccess: (data) => {
      queryClient.setQueryData(queryKeys.profile, data)
      localStorage.setItem('user', JSON.stringify(data))
      toast.success('Profile updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update profile')
    },
  })
}
