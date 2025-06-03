// TypeScript type definitions for the Disaster Response app

export type UserRole = 'affected_individual' | 'volunteer' | 'first_responder' | 'admin'

export type RequestStatus = 'new' | 'processing' | 'prioritized' | 'assigned' | 'in_progress' | 'completed' | 'cancelled'

export type PriorityLevel = 'critical' | 'high' | 'medium' | 'low'

export type TaskStatus = 'pending' | 'assigned' | 'in_progress' | 'completed' | 'cancelled'

export type ResourceType = 'food' | 'water' | 'medical' | 'shelter' | 'transport' | 'personnel' | 'equipment' | 'other'

export type NotificationType = 'info' | 'warning' | 'error' | 'success'

export interface User {
  id: string
  email: string
  full_name?: string
  phone?: string
  role: UserRole
  location?: string
  skills?: string[]
  availability_status: boolean
  is_verified: boolean
  emergency_contact?: string
  medical_info?: string
  created_at: string
  updated_at: string
}

export interface HelpRequest {
  id: string
  user_id: string
  title: string
  description: string
  location?: string
  needs: string[]
  request_type: ResourceType
  priority: PriorityLevel
  urgency_level: PriorityLevel
  urgency_score?: number
  status: RequestStatus
  special_requirements?: string
  people_count: number
  contact_phone?: string
  is_anonymous: boolean
  estimated_response_time?: string
  ai_processed: boolean
  confidence_score?: number
  processed_at?: string
  created_at: string
  updated_at: string
  user?: User
}

export interface Task {
  id: string
  request_id: string
  assigned_to?: string
  assigned_by?: string
  title: string
  description?: string
  task_type: ResourceType
  priority: PriorityLevel
  status: TaskStatus
  location?: string
  required_skills?: string[]
  estimated_duration?: number
  deadline?: string
  completion_notes?: string
  resources_needed?: Record<string, any>
  progress_percentage: number
  created_at: string
  updated_at: string
  completed_at?: string
  request?: HelpRequest
  assigned_user?: User
  assigned_by_user?: User
}

export interface Resource {
  id: string
  type: ResourceType
  name: string
  description?: string
  quantity: number
  unit: string
  threshold: number
  location?: string
  managed_by?: string
  cost_per_unit: number
  supplier?: string
  expiry_date?: string
  is_available: boolean
  created_at: string
  updated_at: string
  manager?: User
}

export interface ResourceConsumption {
  id: string
  resource_id: string
  task_id?: string
  request_id?: string
  quantity_used: number
  used_by?: string
  purpose?: string
  notes?: string
  created_at: string
  resource?: Resource
  task?: Task
  request?: HelpRequest
  user?: User
}

export interface Notification {
  id: string
  user_id: string
  title: string
  message: string
  type: NotificationType
  is_read: boolean
  related_request_id?: string
  related_task_id?: string
  action_url?: string
  created_at: string
  read_at?: string
  related_request?: HelpRequest
  related_task?: Task
}

export interface Communication {
  id: string
  request_id?: string
  task_id?: string
  from_user_id?: string
  to_user_id?: string
  message: string
  communication_type: string
  is_automated: boolean
  created_at: string
  from_user?: User
  to_user?: User
  request?: HelpRequest
  task?: Task
}

export interface AgentLog {
  id: string
  agent_name: string
  action: string
  request_id?: string
  task_id?: string
  input_data?: Record<string, any>
  output_data?: Record<string, any>
  success: boolean
  error_message?: string
  processing_time_ms?: number
  created_at: string
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

// Dashboard statistics
export interface DashboardStats {
  total_requests: number
  active_requests: number
  completed_requests: number
  critical_requests: number
  high_priority_requests: number
  available_volunteers: number
  active_responders: number
  low_stock_resources: number
  recent_requests: HelpRequest[]
  priority_breakdown: Record<PriorityLevel, number>
  status_breakdown: Record<RequestStatus, number>
  resource_status: {
    type: ResourceType
    available: number
    low_stock: boolean
  }[]
}

// Form types
export interface CreateRequestForm {
  title: string
  description: string
  location?: string
  people_count: number
  contact_phone?: string
  special_requirements?: string
  is_anonymous: boolean
  needs: string[]
}

export interface UpdateTaskForm {
  status?: TaskStatus
  progress_percentage?: number
  completion_notes?: string
}

export interface CreateResourceForm {
  type: ResourceType
  name: string
  description?: string
  quantity: number
  unit: string
  threshold: number
  location?: string
  cost_per_unit: number
  supplier?: string
  expiry_date?: string
}

export interface FilterOptions {
  status?: RequestStatus[]
  priority?: PriorityLevel[]
  request_type?: ResourceType[]
  location?: string
  user_role?: UserRole
  assigned_to?: string
  created_after?: string
  created_before?: string
  page?: number
  per_page?: number
  search?: string
}

// Authentication types
export interface AuthUser {
  id: string
  email: string
  role: UserRole
  full_name?: string
  phone?: string
  location?: string
  skills?: string[]
  availability_status: boolean
  is_verified: boolean
}

export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  email: string
  password: string
  full_name: string
  phone?: string
  role: UserRole
  location?: string
  emergency_contact?: string
}

// Error types
export interface ApiError {
  message: string
  code?: string
  details?: Record<string, any>
}

// WebSocket message types
export interface WebSocketMessage {
  type: 'new_request' | 'task_assigned' | 'status_update' | 'notification'
  data: Record<string, any>
  timestamp: string
}

// Chart data types for dashboard
export interface ChartData {
  name: string
  value: number
  fill?: string
}

export interface TimeSeriesData {
  date: string
  requests: number
  completed: number
}

// Agent status types
export interface AgentStatus {
  name: string
  status: 'active' | 'inactive' | 'error'
  last_run?: string
  next_run?: string
  processed_count: number
  error_count: number
}

// Map related types
export interface LocationData {
  latitude: number
  longitude: number
  address?: string
}

export interface MapMarker {
  id: string
  position: LocationData
  type: 'request' | 'resource' | 'responder'
  priority?: PriorityLevel
  status?: RequestStatus
  title: string
  description?: string
}
