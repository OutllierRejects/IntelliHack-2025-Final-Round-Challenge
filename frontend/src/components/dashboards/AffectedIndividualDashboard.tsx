import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { DashboardLayout } from '../layout/DashboardLayout';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { Modal } from '../ui/Modal';
import { Loading } from '../ui/Loading';
import { CreateRequestForm } from '../forms/CreateRequestForm';
import { useRequests, useTasks } from '../../hooks/api';
import { formatDate, getPriorityColor, getStatusColor } from '../../utils';
import { 
  ExclamationTriangleIcon, 
  ClockIcon, 
  CheckCircleIcon,
  PlusIcon,
  MapPinIcon,
  PhoneIcon
} from '@heroicons/react/24/outline';

export const AffectedIndividualDashboard: React.FC = () => {
  const [showCreateRequest, setShowCreateRequest] = useState(false);
  
  const { data: requests, isLoading: requestsLoading } = useRequests();
  const { data: tasks, isLoading: tasksLoading } = useTasks();

  // Filter data for current user
  const myRequests = requests?.filter(req => req.requester_id === 'current_user_id') || [];
  const myTasks = tasks?.filter(task => task.assigned_to === 'current_user_id') || [];

  const stats = [
    {
      name: 'Active Requests',
      value: myRequests.filter(req => req.status === 'open').length.toString(),
      icon: ExclamationTriangleIcon,
      color: 'red',
    },
    {
      name: 'Pending Tasks',
      value: myTasks.filter(task => task.status === 'pending').length.toString(),
      icon: ClockIcon,
      color: 'yellow',
    },
    {
      name: 'Completed Tasks',
      value: myTasks.filter(task => task.status === 'completed').length.toString(),
      icon: CheckCircleIcon,
      color: 'green',
    },
  ];

  const emergencyContacts = [
    { name: 'Emergency Services', number: '911', type: 'emergency' },
    { name: 'Local Emergency Management', number: '(555) 123-4567', type: 'local' },
    { name: 'Red Cross', number: '1-800-733-2767', type: 'support' },
    { name: 'Disaster Hotline', number: '1-800-985-5990', type: 'support' },
  ];

  return (
    <DashboardLayout
      title="My Emergency Status"
      subtitle="Request help and track your situation"
      actions={
        <Button
          onClick={() => setShowCreateRequest(true)}
          className="bg-red-600 hover:bg-red-700 text-white"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          Request Help
        </Button>
      }
    >
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat) => (
          <Card key={stat.name} className="p-6">
            <div className="flex items-center">
              <div className={`p-2 rounded-lg bg-${stat.color}-100`}>
                <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* My Requests */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-medium text-gray-900">My Help Requests</h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowCreateRequest(true)}
              >
                <PlusIcon className="w-4 h-4 mr-1" />
                New Request
              </Button>
            </div>

            {requestsLoading ? (
              <Loading />
            ) : myRequests.length === 0 ? (
              <div className="text-center py-8">
                <ExclamationTriangleIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No requests yet</h3>
                <p className="text-gray-500 mb-4">
                  Create your first request to get help from our response network.
                </p>
                <Button onClick={() => setShowCreateRequest(true)}>
                  Request Help Now
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {myRequests.map((request) => (
                  <div
                    key={request.id}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge color={getPriorityColor(request.priority)}>
                            {request.priority}
                          </Badge>
                          <Badge color={getStatusColor(request.status)}>
                            {request.status}
                          </Badge>
                        </div>
                        <h3 className="text-sm font-medium text-gray-900 mb-1">
                          {request.request_type}
                        </h3>
                        <p className="text-sm text-gray-600 mb-2">
                          {request.description}
                        </p>
                        <div className="flex items-center text-xs text-gray-500 space-x-4">
                          <span className="flex items-center">
                            <MapPinIcon className="w-3 h-3 mr-1" />
                            {request.location}
                          </span>
                          <span>
                            Created {formatDate(request.created_at)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

        {/* Emergency Contacts & Safety Info */}
        <div className="space-y-6">
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Emergency Contacts
            </h2>
            <div className="space-y-3">
              {emergencyContacts.map((contact, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{contact.name}</p>
                    <p className="text-xs text-gray-500">{contact.type}</p>
                  </div>
                  <a
                    href={`tel:${contact.number}`}
                    className="flex items-center text-blue-600 hover:text-blue-800"
                  >
                    <PhoneIcon className="w-4 h-4 mr-1" />
                    <span className="text-sm font-medium">{contact.number}</span>
                  </a>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Safety Tips
            </h2>
            <div className="space-y-3 text-sm text-gray-600">
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="font-medium text-yellow-800 mb-1">Stay Informed</p>
                <p className="text-yellow-700">Monitor local emergency broadcasts and weather alerts.</p>
              </div>
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="font-medium text-blue-800 mb-1">Emergency Kit</p>
                <p className="text-blue-700">Keep water, food, flashlight, and first aid supplies ready.</p>
              </div>
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="font-medium text-green-800 mb-1">Communication</p>
                <p className="text-green-700">Have backup communication methods and emergency contacts.</p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Create Request Modal */}
      <Modal
        isOpen={showCreateRequest}
        onClose={() => setShowCreateRequest(false)}
        title="Request Help"
        maxWidth="2xl"
      >
        <CreateRequestForm
          onSuccess={() => {
            setShowCreateRequest(false);
            // TODO: Refetch requests
          }}
          onCancel={() => setShowCreateRequest(false)}
        />
      </Modal>
    </DashboardLayout>
  );
};
