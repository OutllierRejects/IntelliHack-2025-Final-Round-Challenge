import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { DashboardLayout } from "../layout/DashboardLayout";
import { Card } from "../ui/Card";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import { Loading } from "../ui/Loading";
import { useRequests, useTasks, useResources } from "../../hooks/api";
import { formatDate, getPriorityColor, getStatusColor } from "../../utils";
import {
  HandRaisedIcon,
  ClockIcon,
  CheckCircleIcon,
  UserGroupIcon,
  MapPinIcon,
  PhoneIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";

export const VolunteerDashboard: React.FC = () => {
  const [selectedRequest, setSelectedRequest] = useState<string | null>(null);

  const { data: requests, isLoading: requestsLoading } = useRequests();
  const { data: tasks, isLoading: tasksLoading } = useTasks();
  const { data: resources, isLoading: resourcesLoading } = useResources();

  // Filter data for volunteer
  const availableRequests =
    requests?.filter((req) => req.status === "open") || [];
  const myTasks =
    tasks?.filter((task) => task.assigned_to === "current_user_id") || [];
  const urgentRequests = availableRequests.filter(
    (req) => req.priority === "high"
  );

  const stats = [
    {
      name: "Available Requests",
      value: availableRequests.length.toString(),
      icon: HandRaisedIcon,
      color: "blue",
    },
    {
      name: "My Active Tasks",
      value: myTasks
        .filter((task) => task.status === "in_progress")
        .length.toString(),
      icon: ClockIcon,
      color: "yellow",
    },
    {
      name: "Completed Tasks",
      value: myTasks
        .filter((task) => task.status === "completed")
        .length.toString(),
      icon: CheckCircleIcon,
      color: "green",
    },
    {
      name: "Urgent Requests",
      value: urgentRequests.length.toString(),
      icon: ExclamationTriangleIcon,
      color: "red",
    },
  ];

  const handleAcceptRequest = (requestId: string) => {
    // TODO: Implement accept request logic
    console.log("Accepting request:", requestId);
  };

  return (
    <DashboardLayout
      title="Volunteer Dashboard"
      subtitle="Help coordinate disaster response efforts"
    >
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
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
        {/* Available Requests */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-medium text-gray-900">
                Available Help Requests
              </h2>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm">
                  Filter
                </Button>
                <Button variant="outline" size="sm">
                  Sort
                </Button>
              </div>
            </div>

            {requestsLoading ? (
              <Loading />
            ) : availableRequests.length === 0 ? (
              <div className="text-center py-8">
                <HandRaisedIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No requests available
                </h3>
                <p className="text-gray-500">
                  Check back later for new help requests in your area.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {availableRequests.map((request) => (
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
                          {request.priority === "high" && (
                            <Badge color="red" className="animate-pulse">
                              URGENT
                            </Badge>
                          )}
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
                          <span>{formatDate(request.created_at)}</span>
                          {request.people_count && (
                            <span className="flex items-center">
                              <UserGroupIcon className="w-3 h-3 mr-1" />
                              {request.people_count} people affected
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="ml-4 flex flex-col space-y-2">
                        <Button
                          size="sm"
                          onClick={() => handleAcceptRequest(request.id)}
                        >
                          Accept
                        </Button>
                        <Button variant="outline" size="sm">
                          Details
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* My Current Tasks */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              My Current Tasks
            </h2>
            {tasksLoading ? (
              <Loading size="sm" />
            ) : myTasks.length === 0 ? (
              <p className="text-sm text-gray-500">No active tasks</p>
            ) : (
              <div className="space-y-3">
                {myTasks.slice(0, 3).map((task) => (
                  <div key={task.id} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-medium text-gray-900">
                        {task.title}
                      </h4>
                      <Badge color={getStatusColor(task.status)} size="sm">
                        {task.status}
                      </Badge>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">
                      {task.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-500">
                        Due: {formatDate(task.due_date)}
                      </span>
                      <Button size="xs" variant="outline">
                        Update
                      </Button>
                    </div>
                  </div>
                ))}
                {myTasks.length > 3 && (
                  <Button variant="outline" size="sm" className="w-full">
                    View All Tasks
                  </Button>
                )}
              </div>
            )}
          </Card>

          {/* Resource Availability */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Resource Status
            </h2>
            {resourcesLoading ? (
              <Loading size="sm" />
            ) : (
              <div className="space-y-3">
                {resources?.slice(0, 5).map((resource) => (
                  <div
                    key={resource.id}
                    className="flex items-center justify-between"
                  >
                    <span className="text-sm text-gray-900">
                      {resource.name}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">
                        {resource.current_stock} / {resource.max_capacity}
                      </span>
                      <Badge
                        color={
                          resource.current_stock < resource.low_stock_threshold
                            ? "red"
                            : "green"
                        }
                        size="sm"
                      >
                        {resource.current_stock < resource.low_stock_threshold
                          ? "Low"
                          : "OK"}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Quick Actions */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Quick Actions
            </h2>
            <div className="space-y-2">
              <Button className="w-full justify-start" variant="outline">
                <PhoneIcon className="w-4 h-4 mr-2" />
                Report Status
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <MapPinIcon className="w-4 h-4 mr-2" />
                Update Location
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <UserGroupIcon className="w-4 h-4 mr-2" />
                Request Backup
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
};
