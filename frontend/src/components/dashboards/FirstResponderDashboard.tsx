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
  ExclamationTriangleIcon,
  ClockIcon,
  CheckCircleIcon,
  UserGroupIcon,
  MapPinIcon,
  PhoneIcon,
  ChartBarIcon,
  TruckIcon,
  HeartIcon,
  FireIcon,
} from "@heroicons/react/24/outline";

export const FirstResponderDashboard: React.FC = () => {
  const [activeIncidents, setActiveIncidents] = useState<string[]>([]);

  const { data: requests, isLoading: requestsLoading } = useRequests();
  const { data: tasks, isLoading: tasksLoading } = useTasks();
  const { data: resources, isLoading: resourcesLoading } = useResources();

  // Filter data for first responder
  const criticalRequests =
    requests?.filter(
      (req) => req.priority === "high" && req.status === "open"
    ) || [];
  const myAssignedTasks =
    tasks?.filter((task) => task.assigned_to === "current_user_id") || [];
  const emergencyResources =
    resources?.filter((res) => res.category === "emergency") || [];

  const stats = [
    {
      name: "Critical Incidents",
      value: criticalRequests.length.toString(),
      icon: ExclamationTriangleIcon,
      color: "red",
    },
    {
      name: "Active Responses",
      value: myAssignedTasks
        .filter((task) => task.status === "in_progress")
        .length.toString(),
      icon: ClockIcon,
      color: "blue",
    },
    {
      name: "Resolved Today",
      value: myAssignedTasks
        .filter(
          (task) =>
            task.status === "completed" &&
            new Date(task.updated_at).toDateString() ===
              new Date().toDateString()
        )
        .length.toString(),
      icon: CheckCircleIcon,
      color: "green",
    },
    {
      name: "People Helped",
      value: "47", // TODO: Calculate from completed requests
      icon: UserGroupIcon,
      color: "purple",
    },
  ];

  const incidentTypes = [
    { type: "Medical Emergency", count: 8, icon: HeartIcon, color: "red" },
    { type: "Fire/Explosion", count: 3, icon: FireIcon, color: "orange" },
    { type: "Search & Rescue", count: 12, icon: UserGroupIcon, color: "blue" },
    { type: "Transportation", count: 5, icon: TruckIcon, color: "green" },
  ];

  const handleDispatch = (requestId: string) => {
    // TODO: Implement dispatch logic
    console.log("Dispatching to request:", requestId);
  };

  const handleMarkEnRoute = (taskId: string) => {
    // TODO: Implement en route status update
    console.log("Marking en route:", taskId);
  };

  return (
    <DashboardLayout
      title="First Responder Command"
      subtitle="Emergency response coordination and dispatch"
      actions={
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <MapPinIcon className="w-4 h-4 mr-1" />
            Map View
          </Button>
          <Button className="bg-red-600 hover:bg-red-700 text-white">
            Emergency Protocol
          </Button>
        </div>
      }
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
        {/* Critical Incidents */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-medium text-gray-900">
                Critical Incidents
              </h2>
              <div className="flex items-center space-x-2">
                <Badge color="red" className="animate-pulse">
                  {criticalRequests.length} ACTIVE
                </Badge>
                <Button variant="outline" size="sm">
                  Dispatch All
                </Button>
              </div>
            </div>

            {requestsLoading ? (
              <Loading />
            ) : criticalRequests.length === 0 ? (
              <div className="text-center py-8">
                <CheckCircleIcon className="w-12 h-12 text-green-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No critical incidents
                </h3>
                <p className="text-gray-500">
                  All critical situations are currently being handled.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {criticalRequests.map((request) => (
                  <div
                    key={request.id}
                    className="border-2 border-red-200 rounded-lg p-4 bg-red-50"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge color="red" className="animate-pulse">
                            CRITICAL
                          </Badge>
                          <Badge color={getStatusColor(request.status)}>
                            {request.status}
                          </Badge>
                          <span className="text-xs text-gray-500">
                            ID: {request.id.slice(0, 8)}
                          </span>
                        </div>
                        <h3 className="text-sm font-bold text-gray-900 mb-1">
                          {request.request_type}
                        </h3>
                        <p className="text-sm text-gray-700 mb-2">
                          {request.description}
                        </p>
                        <div className="flex items-center text-xs text-gray-600 space-x-4">
                          <span className="flex items-center font-medium">
                            <MapPinIcon className="w-3 h-3 mr-1" />
                            {request.location}
                          </span>
                          <span>{formatDate(request.created_at)}</span>
                          {request.people_count && (
                            <span className="flex items-center">
                              <UserGroupIcon className="w-3 h-3 mr-1" />
                              {request.people_count} affected
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="ml-4 flex flex-col space-y-2">
                        <Button
                          size="sm"
                          className="bg-red-600 hover:bg-red-700"
                          onClick={() => handleDispatch(request.id)}
                        >
                          Dispatch
                        </Button>
                        <Button variant="outline" size="sm">
                          Details
                        </Button>
                        <Button variant="outline" size="sm">
                          <PhoneIcon className="w-3 h-3" />
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
          {/* Active Responses */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              My Active Responses
            </h2>
            {tasksLoading ? (
              <Loading size="sm" />
            ) : myAssignedTasks.length === 0 ? (
              <p className="text-sm text-gray-500">No active responses</p>
            ) : (
              <div className="space-y-3">
                {myAssignedTasks.slice(0, 4).map((task) => (
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
                        ETA: {formatDate(task.due_date)}
                      </span>
                      <Button
                        size="xs"
                        onClick={() => handleMarkEnRoute(task.id)}
                        disabled={task.status === "completed"}
                      >
                        {task.status === "pending" ? "En Route" : "Update"}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Incident Types */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Incident Types Today
            </h2>
            <div className="space-y-3">
              {incidentTypes.map((incident) => (
                <div
                  key={incident.type}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center">
                    <div
                      className={`p-1 rounded bg-${incident.color}-100 mr-3`}
                    >
                      <incident.icon
                        className={`w-4 h-4 text-${incident.color}-600`}
                      />
                    </div>
                    <span className="text-sm text-gray-900">
                      {incident.type}
                    </span>
                  </div>
                  <Badge color={incident.color} size="sm">
                    {incident.count}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>

          {/* Emergency Resources */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Emergency Resources
            </h2>
            {resourcesLoading ? (
              <Loading size="sm" />
            ) : (
              <div className="space-y-3">
                {emergencyResources.slice(0, 5).map((resource) => (
                  <div
                    key={resource.id}
                    className="flex items-center justify-between"
                  >
                    <span className="text-sm text-gray-900">
                      {resource.name}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">
                        {resource.current_stock}
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
                          : "Ready"}
                      </Badge>
                    </div>
                  </div>
                ))}
                <Button variant="outline" size="sm" className="w-full mt-2">
                  <ChartBarIcon className="w-4 h-4 mr-1" />
                  View All Resources
                </Button>
              </div>
            )}
          </Card>

          {/* Quick Communications */}
          <Card className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Quick Comms
            </h2>
            <div className="space-y-2">
              <Button className="w-full justify-start" variant="outline">
                <PhoneIcon className="w-4 h-4 mr-2" />
                Dispatch Center
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <UserGroupIcon className="w-4 h-4 mr-2" />
                Team Radio
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <ExclamationTriangleIcon className="w-4 h-4 mr-2" />
                Emergency Alert
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
};
