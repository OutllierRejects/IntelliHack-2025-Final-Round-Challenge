-- Sample data for disaster response system
-- This migration adds test data for development and testing
-- Insert sample users
INSERT INTO
  users (
    id,
    email,
    PASSWORD,
    full_name,
    role,
    phone,
    location,
    is_available,
    is_verified,
    created_at
  )
VALUES
  (
    'user-1',
    'admin@disaster.response',
    '$2b$12$LQv3c1yqBw2VdOeLw3h4w.vCwjL5X9lUzH9ZjP5xCjK8Y9iQJ5xKi',
    'Admin User',
    'admin',
    '+1234567890',
    'Emergency HQ',
    TRUE,
    TRUE,
    NOW()
  ),
  (
    'user-2',
    'john.responder@fire.dept',
    '$2b$12$LQv3c1yqBw2VdOeLw3h4w.vCwjL5X9lUzH9ZjP5xCjK8Y9iQJ5xKi',
    'John Smith',
    'first_responder',
    '+1234567891',
    'Fire Station 1',
    TRUE,
    TRUE,
    NOW()
  ),
  (
    'user-3',
    'sarah.volunteer@rescue.org',
    '$2b$12$LQv3c1yqBw2VdOeLw3h4w.vCwjL5X9lUzH9ZjP5xCjK8Y9iQJ5xKi',
    'Sarah Johnson',
    'volunteer',
    '+1234567892',
    'Community Center',
    TRUE,
    TRUE,
    NOW()
  ),
  (
    'user-4',
    'mike.affected@gmail.com',
    '$2b$12$LQv3c1yqBw2VdOeLw3h4w.vCwjL5X9lUzH9ZjP5xCjK8Y9iQJ5xKi',
    'Mike Davis',
    'affected_individual',
    '+1234567893',
    '123 Main St',
    false,
    TRUE,
    NOW()
  ),
  (
    'user-5',
    'emma.volunteer@redcross.org',
    '$2b$12$LQv3c1yqBw2VdOeLw3h4w.vCwjL5X9lUzH9ZjP5xCjK8Y9iQJ5xKi',
    'Emma Wilson',
    'volunteer',
    '+1234567894',
    'Downtown Area',
    TRUE,
    TRUE,
    NOW()
  );

-- Insert sample help requests
INSERT INTO
  help_requests (
    id,
    title,
    description,
    TYPE,
    priority,
    STATUS,
    location,
    contact_phone,
    created_by,
    created_at,
    agent_metadata
  )
VALUES
  (
    'req-1',
    'Family trapped in flooded basement',
    'Family of 4 trapped in basement due to flash flooding. Water level rising rapidly.',
    'rescue',
    'critical',
    'pending',
    '456 Oak Avenue',
    '+1555000001',
    'user-4',
    NOW() - INTERVAL '30 minutes',
    '{"ai_assessment": "Critical rescue situation requiring immediate response", "estimated_resources": ["rescue_boat", "pumping_equipment"]}'
  ),
  (
    'req-2',
    'Medical assistance needed',
    'Elderly person with diabetes needs medication and medical check. Power is out, no transportation available.',
    'medical',
    'high',
    'assigned',
    '789 Pine Street',
    '+1555000002',
    'user-4',
    NOW() - INTERVAL '45 minutes',
    '{"ai_assessment": "Medical priority case", "estimated_time": "2-3 hours"}'
  ),
  (
    'req-3',
    'Food and water for displaced family',
    'Family of 5 lost home in fire, need temporary shelter and basic supplies.',
    'supplies',
    'medium',
    'pending',
    'Red Cross Shelter',
    '+1555000003',
    'user-4',
    NOW() - INTERVAL '2 hours',
    '{"ai_assessment": "Basic needs support", "shelter_capacity": "available"}'
  ),
  (
    'req-4',
    'Road clearance needed',
    'Large tree blocking main evacuation route on Highway 101.',
    'infrastructure',
    'high',
    'in_progress',
    'Highway 101 Mile Marker 15',
    '+1555000004',
    'user-4',
    NOW() - INTERVAL '1 hour',
    '{"ai_assessment": "Infrastructure priority - affects evacuation routes"}'
  );

-- Insert sample tasks
INSERT INTO
  tasks (
    id,
    title,
    description,
    TYPE,
    priority,
    STATUS,
    request_id,
    assigned_to,
    created_by,
    estimated_time,
    created_at
  )
VALUES
  (
    'task-1',
    'Emergency water rescue',
    'Deploy rescue team to assist trapped family in flooded basement',
    'rescue',
    'critical',
    'assigned',
    'req-1',
    'user-2',
    'user-1',
    120,
    NOW() - INTERVAL '25 minutes'
  ),
  (
    'task-2',
    'Medical assessment and supply delivery',
    'Provide medical check and deliver insulin to elderly diabetic patient',
    'medical',
    'high',
    'in_progress',
    'req-2',
    'user-3',
    'user-1',
    180,
    NOW() - INTERVAL '40 minutes'
  ),
  (
    'task-3',
    'Tree removal - Highway 101',
    'Clear fallen tree from evacuation route',
    'infrastructure',
    'high',
    'assigned',
    'req-4',
    'user-2',
    'user-1',
    240,
    NOW() - INTERVAL '55 minutes'
  ),
  (
    'task-4',
    'Supply distribution setup',
    'Set up food and supply distribution point at community center',
    'logistics',
    'medium',
    'pending',
    NULL,
    NULL,
    'user-1',
    300,
    NOW() - INTERVAL '1 hour'
  );

-- Insert sample resources
INSERT INTO
  resources (
    id,
    name,
    TYPE,
    quantity,
    unit,
    location,
    description,
    minimum_stock,
    created_by,
    created_at
  )
VALUES
  (
    'res-1',
    'Emergency Water Bottles',
    'food',
    500,
    'bottles',
    'Warehouse A',
    '16oz emergency water bottles',
    100,
    'user-1',
    NOW()
  ),
  (
    'res-2',
    'First Aid Kits',
    'medical',
    25,
    'kits',
    'Medical Supply Room',
    'Complete first aid kits with bandages, antiseptic, etc.',
    10,
    'user-1',
    NOW()
  ),
  (
    'res-3',
    'Emergency Blankets',
    'shelter',
    200,
    'pieces',
    'Warehouse B',
    'Thermal emergency blankets',
    50,
    'user-1',
    NOW()
  ),
  (
    'res-4',
    'Rescue Boats',
    'equipment',
    3,
    'units',
    'Fire Station 1',
    'Inflatable rescue boats with motors',
    1,
    'user-1',
    NOW()
  ),
  (
    'res-5',
    'Portable Generators',
    'equipment',
    8,
    'units',
    'Equipment Storage',
    '5000W portable generators',
    2,
    'user-1',
    NOW()
  ),
  (
    'res-6',
    'MRE Meals',
    'food',
    1000,
    'meals',
    'Food Storage',
    'Ready-to-eat meals for emergency distribution',
    200,
    'user-1',
    NOW()
  );

-- Insert sample notifications
INSERT INTO
  notifications (
    id,
    user_id,
    title,
    message,
    TYPE,
    priority,
    is_read,
    created_at
  )
VALUES
  (
    'notif-1',
    'user-2',
    'New Critical Task Assigned',
    'Emergency water rescue task assigned to you - family trapped in basement',
    'task_assigned',
    'critical',
    false,
    NOW() - INTERVAL '25 minutes'
  ),
  (
    'notif-2',
    'user-3',
    'Task In Progress Update',
    'Medical assessment task is now in progress',
    'task_updated',
    'medium',
    false,
    NOW() - INTERVAL '40 minutes'
  ),
  (
    'notif-3',
    'user-1',
    'New Emergency Request',
    'Critical rescue request received from 456 Oak Avenue',
    'request_created',
    'high',
    TRUE,
    NOW() - INTERVAL '30 minutes'
  ),
  (
    'notif-4',
    'user-5',
    'Low Stock Alert',
    'First Aid Kits are running low (15 remaining)',
    'resource_alert',
    'medium',
    false,
    NOW() - INTERVAL '2 hours'
  );

-- Insert sample resource usage records
INSERT INTO
  resource_usage (
    id,
    resource_id,
    task_id,
    quantity_used,
    purpose,
    used_by,
    created_at
  )
VALUES
  (
    'usage-1',
    'res-2',
    'task-2',
    1,
    'Medical assistance for diabetic patient',
    'user-3',
    NOW() - INTERVAL '35 minutes'
  ),
  (
    'usage-2',
    'res-4',
    'task-1',
    1,
    'Water rescue operation',
    'user-2',
    NOW() - INTERVAL '20 minutes'
  ),
  (
    'usage-3',
    'res-1',
    'task-2',
    10,
    'Emergency water supply for patient',
    'user-3',
    NOW() - INTERVAL '30 minutes'
  );

-- Insert sample agent workflow records  
INSERT INTO
  agent_workflows (
    id,
    request_id,
    workflow_type,
    STATUS,
    current_step,
    steps_completed,
    ai_insights,
    started_at,
    updated_at
  )
VALUES
  (
    'workflow-1',
    'req-1',
    'emergency_response',
    'active',
    'assignment',
    2,
    '{"priority_score": 95, "resource_requirements": ["rescue_boat", "medical_kit"], "estimated_completion": "2024-01-15T15:30:00Z"}',
    NOW() - INTERVAL '25 minutes',
    NOW() - INTERVAL '20 minutes'
  ),
  (
    'workflow-2',
    'req-2',
    'medical_assistance',
    'active',
    'execution',
    3,
    '{"medical_priority": 85, "required_supplies": ["insulin", "glucose_monitor"], "estimated_completion": "2024-01-15T16:00:00Z"}',
    NOW() - INTERVAL '40 minutes',
    NOW() - INTERVAL '35 minutes'
  ),
  (
    'workflow-3',
    'req-3',
    'supply_distribution',
    'pending',
    'intake',
    1,
    '{"family_size": 5, "required_supplies": ["food", "clothing", "temporary_shelter"], "priority_score": 60}',
    NOW() - INTERVAL '2 hours',
    NOW() - INTERVAL '2 hours'
  );

-- Update user passwords (these are hashed versions of 'password123')
-- Note: In production, use proper password hashing
COMMENT ON TABLE users IS 'Sample users created with password: password123';

-- Insert some dashboard stats for testing
INSERT INTO
  dashboard_stats (
    id,
    total_requests,
    active_requests,
    completed_requests,
    available_volunteers,
    active_tasks,
    low_stock_resources,
    last_updated
  )
VALUES
  (1, 4, 2, 0, 2, 3, 1, NOW());

COMMIT;
