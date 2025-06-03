-- Sample data for testing the Disaster Response Coordination App
-- Migration: 002_sample_data.sql

-- Insert sample user profiles (these would normally be created through Supabase auth)
-- Note: In production, these IDs would come from auth.users table
INSERT INTO public.user_profiles (id, email, full_name, phone, role, location, skills, availability_status, is_verified) VALUES
-- Admin users
('a0000000-0000-0000-0000-000000000001', 'admin@disaster-response.org', 'System Administrator', '+1-555-0001', 'admin', 'Emergency Operations Center', '{"management", "coordination", "system_admin"}', true, true),

-- First responders
('b0000000-0000-0000-0000-000000000001', 'fire.chief@city.gov', 'Fire Chief Johnson', '+1-555-1001', 'first_responder', 'Fire Station 1', '{"fire_suppression", "rescue", "medical_response", "leadership"}', true, true),
('b0000000-0000-0000-0000-000000000002', 'paramedic.smith@hospital.org', 'Paramedic Sarah Smith', '+1-555-1002', 'first_responder', 'City Hospital', '{"emergency_medical", "trauma_care", "patient_transport"}', true, true),
('b0000000-0000-0000-0000-000000000003', 'police.sergeant@pd.gov', 'Sergeant Mike Davis', '+1-555-1003', 'first_responder', 'Police Station', '{"crowd_control", "evacuation", "security", "investigation"}', true, true),

-- Volunteers
('c0000000-0000-0000-0000-000000000001', 'volunteer.jones@email.com', 'Mary Jones', '+1-555-2001', 'volunteer', 'Community Center', '{"first_aid", "food_distribution", "shelter_management"}', true, true),
('c0000000-0000-0000-0000-000000000002', 'volunteer.brown@email.com', 'David Brown', '+1-555-2002', 'volunteer', 'Red Cross Chapter', '{"logistics", "supply_management", "transportation"}', true, true),
('c0000000-0000-0000-0000-000000000003', 'volunteer.wilson@email.com', 'Lisa Wilson', '+1-555-2003', 'volunteer', 'Local Church', '{"counseling", "childcare", "language_translation"}', false, true),

-- Affected individuals
('d0000000-0000-0000-0000-000000000001', 'resident.garcia@email.com', 'Carlos Garcia', '+1-555-3001', 'affected_individual', '123 Oak Street', NULL, true, true),
('d0000000-0000-0000-0000-000000000002', 'resident.johnson@email.com', 'Amanda Johnson', '+1-555-3002', 'affected_individual', '456 Pine Avenue', NULL, true, true),
('d0000000-0000-0000-0000-000000000003', 'resident.kim@email.com', 'elderly.kim@email.com', '+1-555-3003', 'affected_individual', '789 Elm Street', NULL, true, true);

-- Insert sample resources
INSERT INTO public.resources (type, name, description, quantity, unit, threshold, location, managed_by, cost_per_unit, is_available) VALUES
-- Food resources
('food', 'Emergency Food Kits', 'Ready-to-eat meals for 3 days per person', 250, 'kits', 50, 'Emergency Warehouse A', 'c0000000-0000-0000-0000-000000000002', 15.00, true),
('food', 'Bottled Water Cases', '24-pack of 16oz water bottles', 180, 'cases', 30, 'Emergency Warehouse A', 'c0000000-0000-0000-0000-000000000002', 8.00, true),
('food', 'Baby Formula', 'Infant formula containers', 45, 'containers', 10, 'Community Center', 'c0000000-0000-0000-0000-000000000001', 12.00, true),

-- Medical resources
('medical', 'First Aid Kits', 'Complete first aid supplies', 75, 'kits', 15, 'City Hospital', 'b0000000-0000-0000-0000-000000000002', 25.00, true),
('medical', 'Emergency Medications', 'Basic emergency medication supply', 120, 'units', 20, 'City Hospital', 'b0000000-0000-0000-0000-000000000002', 50.00, true),
('medical', 'Oxygen Tanks', 'Portable oxygen cylinders', 25, 'tanks', 5, 'Fire Station 1', 'b0000000-0000-0000-0000-000000000001', 75.00, true),

-- Shelter resources
('shelter', 'Emergency Blankets', 'Thermal emergency blankets', 300, 'blankets', 50, 'Community Center', 'c0000000-0000-0000-0000-000000000001', 5.00, true),
('shelter', 'Temporary Tents', '4-person emergency tents', 40, 'tents', 10, 'Emergency Warehouse B', 'c0000000-0000-0000-0000-000000000002', 85.00, true),
('shelter', 'Sleeping Bags', 'Cold weather sleeping bags', 150, 'bags', 25, 'Community Center', 'c0000000-0000-0000-0000-000000000001', 35.00, true),

-- Transport resources
('transport', 'Emergency Vehicles', 'Ambulances and rescue vehicles', 8, 'vehicles', 2, 'Fire Station 1', 'b0000000-0000-0000-0000-000000000001', 0.00, true),
('transport', 'Evacuation Buses', 'Large capacity buses for evacuation', 5, 'buses', 1, 'Transit Center', 'b0000000-0000-0000-0000-000000000003', 0.00, true),

-- Equipment
('equipment', 'Generators', 'Portable power generators', 15, 'units', 3, 'Emergency Warehouse B', 'c0000000-0000-0000-0000-000000000002', 450.00, true),
('equipment', 'Communication Radios', 'Two-way emergency radios', 60, 'radios', 10, 'Emergency Operations Center', 'a0000000-0000-0000-0000-000000000001', 125.00, true);

-- Insert sample help requests
INSERT INTO public.requests (user_id, title, description, location, needs, request_type, priority, status, people_count, contact_phone, special_requirements) VALUES
-- Critical requests
('d0000000-0000-0000-0000-000000000001', 'Elderly neighbor needs medical attention', 'My elderly neighbor Mrs. Chen has fallen and cannot get up. She is conscious but in pain and cannot move her leg. Need immediate medical assistance.', '789 Elm Street, Apt 2B', '{"medical", "transport"}', 'medical', 'critical', 'new', 1, '+1-555-3001', 'Elderly, potential fracture, lives alone'),

('d0000000-0000-0000-0000-000000000002', 'Family trapped in flooded basement', 'Our family of 4 is trapped in our basement due to rising flood waters. Water is still rising and we cannot get out safely. Need immediate rescue.', '456 Pine Avenue', '{"rescue", "transport"}', 'rescue', 'critical', 'new', 4, '+1-555-3002', 'Includes 2 young children ages 6 and 8'),

-- High priority requests
('d0000000-0000-0000-0000-000000000003', 'Diabetic running out of insulin', 'I am diabetic and my insulin supply was destroyed in the flood. I have about 2 days worth left and cannot access my pharmacy. Need medical supplies urgently.', '123 Oak Street', '{"medical"}', 'medical', 'high', 'new', 1, '+1-555-3003', 'Diabetic, requires insulin, pharmacy inaccessible'),

-- Medium priority requests
('d0000000-0000-0000-0000-000000000001', 'Need food and water for family', 'Our home was evacuated and we are staying at the community center. We need food and water supplies for our family of 5 for the next few days.', 'Community Center - Evacuation Shelter', '{"food", "water"}', 'food', 'medium', 'new', 5, '+1-555-3001', 'Family with young children'),

('d0000000-0000-0000-0000-000000000002', 'Power outage - need generator', 'We have been without power for 3 days. We have a newborn baby and need power for medical equipment and formula preparation.', '456 Pine Avenue', '{"equipment", "shelter"}', 'equipment', 'medium', 'new', 3, '+1-555-3002', 'Newborn baby, medical equipment required'),

-- Low priority requests
('d0000000-0000-0000-0000-000000000003', 'Temporary shelter needed', 'Our apartment building has been condemned and we need temporary shelter arrangements. We have some supplies but need a place to stay.', '789 Elm Street', '{"shelter"}', 'shelter', 'low', 'new', 2, '+1-555-3003', 'Building condemned, has some personal supplies');

-- Insert sample tasks (some would be auto-generated by assignment agent)
INSERT INTO public.tasks (request_id, assigned_to, assigned_by, title, description, task_type, priority, status, location, required_skills, estimated_duration, resources_needed) VALUES
-- Critical tasks
((SELECT id FROM public.requests WHERE title = 'Elderly neighbor needs medical attention'), 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Emergency Medical Response', 'Respond to elderly fall victim with potential fracture', 'medical', 'critical', 'assigned', '789 Elm Street, Apt 2B', '{"emergency_medical", "patient_assessment", "trauma_care"}', 30, '{"medical": {"First Aid Kits": 1, "Emergency Medications": 1}, "transport": {"Emergency Vehicles": 1}}'),

((SELECT id FROM public.requests WHERE title = 'Family trapped in flooded basement'), 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Water Rescue Operation', 'Extract family of 4 from flooded basement', 'rescue', 'critical', 'assigned', '456 Pine Avenue', '{"water_rescue", "emergency_response", "evacuation"}', 45, '{"transport": {"Emergency Vehicles": 2}, "equipment": {"Communication Radios": 4}}'),

-- High priority tasks  
((SELECT id FROM public.requests WHERE title = 'Diabetic running out of insulin'), 'c0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000002', 'Medical Supply Delivery', 'Deliver insulin and diabetic supplies', 'medical', 'high', 'pending', '123 Oak Street', '{"medical_knowledge", "supply_distribution"}', 20, '{"medical": {"Emergency Medications": 1}}'),

-- Medium priority tasks
((SELECT id FROM public.requests WHERE title = 'Need food and water for family'), 'c0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Family Supply Distribution', 'Distribute food and water supplies to evacuated family', 'food', 'medium', 'pending', 'Community Center - Evacuation Shelter', '{"supply_distribution", "logistics"}', 25, '{"food": {"Emergency Food Kits": 5, "Bottled Water Cases": 2}}');

-- Insert sample notifications
INSERT INTO public.notifications (user_id, title, message, type, related_request_id, is_read) VALUES
-- For responders
('b0000000-0000-0000-0000-000000000002', 'Critical Medical Emergency Assigned', 'You have been assigned a critical medical emergency at 789 Elm Street. Elderly patient with potential fracture.', 'error', (SELECT id FROM public.requests WHERE title = 'Elderly neighbor needs medical attention'), false),
('b0000000-0000-0000-0000-000000000001', 'Water Rescue Operation Assigned', 'Family of 4 trapped in flooded basement requires immediate rescue response.', 'error', (SELECT id FROM public.requests WHERE title = 'Family trapped in flooded basement'), false),

-- For volunteers
('c0000000-0000-0000-0000-000000000001', 'Medical Supply Task Available', 'Diabetic patient needs insulin delivery. High priority medical supply task available.', 'warning', (SELECT id FROM public.requests WHERE title = 'Diabetic running out of insulin'), false),
('c0000000-0000-0000-0000-000000000002', 'Family Needs Food Supplies', 'Family of 5 at evacuation center needs food and water distribution.', 'info', (SELECT id FROM public.requests WHERE title = 'Need food and water for family'), false),

-- For affected individuals
('d0000000-0000-0000-0000-000000000001', 'Help Request Received', 'Your request for medical assistance has been received and assigned to Paramedic Sarah Smith.', 'success', (SELECT id FROM public.requests WHERE title = 'Elderly neighbor needs medical attention'), false),
('d0000000-0000-0000-0000-000000000002', 'Rescue Team Dispatched', 'Fire Chief Johnson has been dispatched for your emergency rescue situation. Help is on the way.', 'success', (SELECT id FROM public.requests WHERE title = 'Family trapped in flooded basement'), false);

-- Insert sample communications
INSERT INTO public.communications (request_id, from_user_id, to_user_id, message, communication_type, is_automated) VALUES
-- Automated system communications
((SELECT id FROM public.requests WHERE title = 'Elderly neighbor needs medical attention'), 'a0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000002', 'Critical medical emergency assigned to you. Patient: Elderly with potential fracture at 789 Elm Street, Apt 2B.', 'assignment', true),
((SELECT id FROM public.requests WHERE title = 'Family trapped in flooded basement'), 'a0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'Water rescue operation assigned. Family of 4 trapped in basement at 456 Pine Avenue.', 'assignment', true),

-- Manual communications
((SELECT id FROM public.requests WHERE title = 'Diabetic running out of insulin'), 'b0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', 'Mary, can you handle the insulin delivery to Oak Street? Patient is stable but needs medication within 24 hours.', 'message', false),
((SELECT id FROM public.requests WHERE title = 'Need food and water for family'), 'c0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000002', 'David, I have the family registered at the shelter. Can you coordinate the supply delivery from the warehouse?', 'message', false);

-- Insert sample resource consumption records
INSERT INTO public.resource_consumption (resource_id, task_id, quantity_used, used_by, purpose, notes) VALUES
-- Medical supplies used
((SELECT id FROM public.resources WHERE name = 'First Aid Kits'), (SELECT id FROM public.tasks WHERE title = 'Emergency Medical Response'), 1, 'b0000000-0000-0000-0000-000000000002', 'Elderly fall victim treatment', 'Basic first aid for potential fracture stabilization'),

-- Equipment deployment
((SELECT id FROM public.resources WHERE name = 'Communication Radios'), (SELECT id FROM public.tasks WHERE title = 'Water Rescue Operation'), 4, 'b0000000-0000-0000-0000-000000000001', 'Rescue team coordination', 'Radios deployed for rescue team communication');

-- Insert sample agent logs
INSERT INTO public.agent_logs (agent_name, action, request_id, input_data, output_data, success, processing_time_ms) VALUES
('IntakeAgent', 'process_request', (SELECT id FROM public.requests WHERE title = 'Elderly neighbor needs medical attention'), 
'{"title": "Elderly neighbor needs medical attention", "description": "My elderly neighbor Mrs. Chen has fallen and cannot get up"}', 
'{"needs": ["medical", "transport"], "priority": "critical", "urgency_level": "critical", "ai_processed": true, "confidence_score": 0.95}', 
true, 1250),

('PrioritizationAgent', 'prioritize_request', (SELECT id FROM public.requests WHERE title = 'Family trapped in flooded basement'),
'{"needs": ["rescue", "transport"], "description": "family trapped in flooded basement", "people_count": 4}',
'{"priority": "critical", "urgency_score": 0.98, "resource_impact": "high", "estimated_response_time": "immediate"}',
true, 850),

('AssignmentAgent', 'assign_task', (SELECT id FROM public.requests WHERE title = 'Diabetic running out of insulin'),
'{"request_type": "medical", "priority": "high", "location": "123 Oak Street", "skills_required": ["medical_knowledge"]}',
'{"assigned_to": "c0000000-0000-0000-0000-000000000001", "confidence": 0.85, "reasoning": "Volunteer with medical knowledge available in area"}',
true, 950);
