-- Disaster Response Coordination App - Initial Database Schema
-- Migration: 001_initial_schema.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable Row Level Security
ALTER DATABASE postgres SET row_security = on;

-- Create enum types
CREATE TYPE user_role AS ENUM ('affected_individual', 'volunteer', 'first_responder', 'admin');
CREATE TYPE request_status AS ENUM ('new', 'processing', 'prioritized', 'assigned', 'in_progress', 'completed', 'cancelled');
CREATE TYPE priority_level AS ENUM ('critical', 'high', 'medium', 'low');
CREATE TYPE task_status AS ENUM ('pending', 'assigned', 'in_progress', 'completed', 'cancelled');
CREATE TYPE resource_type AS ENUM ('food', 'water', 'medical', 'shelter', 'transport', 'personnel', 'equipment', 'other');

-- Users table (extends Supabase auth.users)
CREATE TABLE public.user_profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    role user_role NOT NULL DEFAULT 'affected_individual',
    location VARCHAR(255),
    skills TEXT[], -- Array of skills for volunteers/responders
    availability_status BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    emergency_contact VARCHAR(255),
    medical_info TEXT, -- Emergency medical information
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- Help requests table
CREATE TABLE public.requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    needs TEXT[] DEFAULT '{}', -- Array of needs (food, water, medical, etc.)
    request_type resource_type DEFAULT 'other',
    priority priority_level DEFAULT 'medium',
    urgency_level priority_level DEFAULT 'medium',
    urgency_score DECIMAL(3,2) DEFAULT 0.5,
    status request_status DEFAULT 'new',
    special_requirements TEXT,
    people_count INTEGER DEFAULT 1,
    contact_phone VARCHAR(20),
    is_anonymous BOOLEAN DEFAULT false,
    estimated_response_time VARCHAR(50),
    ai_processed BOOLEAN DEFAULT false,
    confidence_score DECIMAL(3,2) DEFAULT 0.0,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resources table
CREATE TABLE public.resources (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    type resource_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    unit VARCHAR(50) DEFAULT 'units',
    threshold INTEGER DEFAULT 10, -- Low stock threshold
    location VARCHAR(255),
    managed_by UUID REFERENCES public.user_profiles(id),
    cost_per_unit DECIMAL(10,2) DEFAULT 0.00,
    supplier VARCHAR(255),
    expiry_date DATE,
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table
CREATE TABLE public.tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    request_id UUID NOT NULL REFERENCES public.requests(id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES public.user_profiles(id),
    assigned_by UUID REFERENCES public.user_profiles(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    task_type resource_type DEFAULT 'other',
    priority priority_level DEFAULT 'medium',
    status task_status DEFAULT 'pending',
    location VARCHAR(255),
    required_skills TEXT[],
    estimated_duration INTEGER, -- in minutes
    deadline TIMESTAMP WITH TIME ZONE,
    completion_notes TEXT,
    resources_needed JSONB DEFAULT '{}', -- JSON object of resource requirements
    progress_percentage INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Resource consumption tracking
CREATE TABLE public.resource_consumption (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    resource_id UUID NOT NULL REFERENCES public.resources(id) ON DELETE CASCADE,
    task_id UUID REFERENCES public.tasks(id),
    request_id UUID REFERENCES public.requests(id),
    quantity_used INTEGER NOT NULL,
    used_by UUID REFERENCES public.user_profiles(id),
    purpose VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications table
CREATE TABLE public.notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'info', -- info, warning, error, success
    is_read BOOLEAN DEFAULT false,
    related_request_id UUID REFERENCES public.requests(id),
    related_task_id UUID REFERENCES public.tasks(id),
    action_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE
);

-- Communication log
CREATE TABLE public.communications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    request_id UUID REFERENCES public.requests(id),
    task_id UUID REFERENCES public.tasks(id),
    from_user_id UUID REFERENCES public.user_profiles(id),
    to_user_id UUID REFERENCES public.user_profiles(id),
    message TEXT NOT NULL,
    communication_type VARCHAR(50) DEFAULT 'message', -- message, status_update, assignment, completion
    is_automated BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent activity log
CREATE TABLE public.agent_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    request_id UUID REFERENCES public.requests(id),
    task_id UUID REFERENCES public.tasks(id),
    input_data JSONB,
    output_data JSONB,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_requests_status ON public.requests(status);
CREATE INDEX idx_requests_priority ON public.requests(priority);
CREATE INDEX idx_requests_user_id ON public.requests(user_id);
CREATE INDEX idx_requests_created_at ON public.requests(created_at);
CREATE INDEX idx_requests_location ON public.requests(location);

CREATE INDEX idx_tasks_status ON public.tasks(status);
CREATE INDEX idx_tasks_assigned_to ON public.tasks(assigned_to);
CREATE INDEX idx_tasks_request_id ON public.tasks(request_id);
CREATE INDEX idx_tasks_priority ON public.tasks(priority);

CREATE INDEX idx_resources_type ON public.resources(type);
CREATE INDEX idx_resources_availability ON public.resources(is_available);
CREATE INDEX idx_resources_quantity ON public.resources(quantity);

CREATE INDEX idx_notifications_user_id_read ON public.notifications(user_id, is_read);
CREATE INDEX idx_notifications_created_at ON public.notifications(created_at);

CREATE INDEX idx_user_profiles_role ON public.user_profiles(role);
CREATE INDEX idx_user_profiles_availability ON public.user_profiles(availability_status);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_requests_updated_at BEFORE UPDATE ON public.requests FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON public.tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_resources_updated_at BEFORE UPDATE ON public.resources FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security Policies
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.communications ENABLE ROW LEVEL SECURITY;

-- User profiles: Users can read all profiles but only update their own
CREATE POLICY "Users can view all profiles" ON public.user_profiles FOR SELECT USING (true);
CREATE POLICY "Users can update own profile" ON public.user_profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.user_profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Requests: Users can CRUD their own requests, responders/admins can view all
CREATE POLICY "Users can view own requests" ON public.requests FOR SELECT USING (
    auth.uid() = user_id OR 
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role IN ('first_responder', 'admin'))
);
CREATE POLICY "Users can create requests" ON public.requests FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own requests" ON public.requests FOR UPDATE USING (
    auth.uid() = user_id OR 
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role IN ('first_responder', 'admin'))
);

-- Tasks: Assigned users, admins, and responders can view/update
CREATE POLICY "Task visibility" ON public.tasks FOR SELECT USING (
    auth.uid() = assigned_to OR 
    auth.uid() = assigned_by OR
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role IN ('first_responder', 'admin')) OR
    EXISTS (SELECT 1 FROM public.requests WHERE id = request_id AND user_id = auth.uid())
);
CREATE POLICY "Task management" ON public.tasks FOR ALL USING (
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role IN ('first_responder', 'admin'))
);

-- Resources: Admins and responders can manage, others can view
CREATE POLICY "Resource visibility" ON public.resources FOR SELECT USING (true);
CREATE POLICY "Resource management" ON public.resources FOR ALL USING (
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role IN ('first_responder', 'admin'))
);

-- Notifications: Users can only see their own
CREATE POLICY "Own notifications only" ON public.notifications FOR ALL USING (auth.uid() = user_id);

-- Communications: Participants can view their communications
CREATE POLICY "Communication access" ON public.communications FOR SELECT USING (
    auth.uid() = from_user_id OR 
    auth.uid() = to_user_id OR
    EXISTS (SELECT 1 FROM public.user_profiles WHERE id = auth.uid() AND role = 'admin')
);
