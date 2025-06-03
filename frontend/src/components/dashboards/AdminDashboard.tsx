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
  ChartBarIcon,
  CogIcon,
  BellIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";

export const AdminDashboard: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<
    "overview" | "requests" | "resources" | "users"
  >("overview");

  const { data: requests, isLoading: requestsLoading } = useRequests();
  const { data: tasks, isLoading: tasksLoading } = useTasks();
  const { data: resources, isLoading: resourcesLoading } = useResources();

  // Calculate statistics
  const totalRequests = requests?.length || 0;
  const openRequests =
    requests?.filter((req) => req.status === "open").length || 0;
  const criticalRequests =
    requests?.filter((req) => req.priority === "high").length || 0;
  const activeTasks =
    tasks?.filter((task) => task.status === "in_progress").length || 0;
  const completedTasks =
    tasks?.filter((task) => task.status === "completed").length || 0;
  const lowStockResources =
    resources?.filter((res) => res.current_stock < res.low_stock_threshold)
      .length || 0;

  const stats = [
    {
      name: "Total Requests",
      value: totalRequests.toString(),
      change: "+12%",
      changeType: "increase",
      icon: ExclamationTriangleIcon,
      color: "blue",
    },
    {
      name: "Open Requests",
      value: openRequests.toString(),
      change: "-8%",
      changeType: "decrease",
      icon: ClockIcon,
      color: "yellow",
    },
    {
      name: "Critical Incidents",
      value: criticalRequests.toString(),
      change: "+3",
      changeType: "increase",
      icon: ExclamationTriangleIcon,
      color: "red",
    },
    {
      name: "Active Responses",
      value: activeTasks.toString(),
      change: "+15%",
      changeType: "increase",
      icon: UserGroupIcon,
      color: "green",
    },
    {
      name: "Completed Today",
      value: completedTasks.toString(),
      change: "+23%",
      changeType: "increase",
      icon: CheckCircleIcon,
      color: "green",
    },
    {
      name: "Low Stock Items",
      value: lowStockResources.toString(),
      change: "-2",
      changeType: "decrease",
      icon: ChartBarIcon,
      color: lowStockResources > 0 ? "red" : "green",
    },
  ];

  const recentActivity = [
    {
      type: "request",
      message: "New medical emergency request in Downtown",
      time: "2 min ago",
      priority: "high",
    },
    {
      type: "task",
      message: "Rescue team dispatched to Flood Zone A",
      time: "5 min ago",
      priority: "medium",
    },
    {
      type: "resource",
      message: "Medical supplies restocked at Station 3",
      time: "15 min ago",
      priority: "low",
    },
    {
      type: "user",
      message: "New volunteer registered: John Smith",
      time: "1 hour ago",
      priority: "low",
    },
    {
      type: "request",
      message: "Shelter request completed in North District",
      time: "2 hours ago",
      priority: "medium",
    },
  ];

  const agentStatus = [
    {
      name: "Intake Agent",
      status: "active",
      processed: 127,
      lastActive: "30 seconds ago",
    },
    {
      name: "Prioritization Agent",
      status: "active",
      processed: 89,
      lastActive: "1 minute ago",
    },
    {
      name: "Assignment Agent",
      status: "active",
      processed: 76,
      lastActive: "45 seconds ago",
    },
    {
      name: "Communication Agent",
      status: "active",
      processed: 203,
      lastActive: "15 seconds ago",
    },
  ];

  return (
    <DashboardLayout
      title="Admin Command Center"
      subtitle="System overview and management"
      actions={
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <ChartBarIcon className="w-4 h-4 mr-1" />
            Reports
          </Button>
          <Button variant="outline" size="sm">
            <CogIcon className="w-4 h-4 mr-1" />
            Settings
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            <BellIcon className="w-4 h-4 mr-1" />
            Alerts
          </Button>
        </div>
      }
    >
      {/* Navigation Tabs */}
      <div className="mb-8">
        <nav className="flex space-x-8">
          {[
            { id: "overview", name: "Overview" },
            { id: "requests", name: "Requests" },
            { id: "resources", name: "Resources" },
            { id: "users", name: "Users" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                selectedTab === tab.id
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {selectedTab === "overview" && (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {stats.map((stat) => (
              <Card key={stat.name} className="p-6">
                <div className="flex items-center">
                  <div className={`p-2 rounded-lg bg-${stat.color}-100`}>
                    <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
                  </div>
                  <div className="ml-4 flex-1">
                    <p className="text-sm font-medium text-gray-500">
                      {stat.name}
                    </p>
                    <div className="flex items-center">
                      <p className="text-2xl font-bold text-gray-900">
                        {stat.value}
                      </p>
                      <span
                        className={`ml-2 text-sm font-medium ${
                          stat.changeType === "increase"
                            ? "text-green-600"
                            : "text-red-600"
                        }`}
                      >
                        {stat.change}
                      </span>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Recent Activity */}
            <div className="lg:col-span-2">
              <Card className="p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  Recent Activity
                </h2>
                <div className="space-y-4">
                  {recentActivity.map((activity, index) => (
                    <div
                      key={index}
                      className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <div
                        className={`p-1 rounded-full ${
                          activity.priority === "high"
                            ? "bg-red-100"
                            : activity.priority === "medium"
                            ? "bg-yellow-100"
                            : "bg-gray-100"
                        }`}
                      >
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.priority === "high"
                              ? "bg-red-500"
                              : activity.priority === "medium"
                              ? "bg-yellow-500"
                              : "bg-gray-500"
                          }`}
                        />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">
                          {activity.message}
                        </p>
                        <p className="text-xs text-gray-500">{activity.time}</p>
                      </div>
                      <Badge
                        color={
                          activity.priority === "high"
                            ? "red"
                            : activity.priority === "medium"
                            ? "yellow"
                            : "gray"
                        }
                        size="sm"
                      >
                        {activity.type}
                      </Badge>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            {/* Agent Status */}
            <div>
              <Card className="p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  AI Agent Status
                </h2>
                <div className="space-y-4">
                  {agentStatus.map((agent) => (
                    <div key={agent.name} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-sm font-medium text-gray-900">
                          {agent.name}
                        </h3>
                        <Badge
                          color={agent.status === "active" ? "green" : "red"}
                          size="sm"
                        >
                          {agent.status}
                        </Badge>
                      </div>
                      <div className="text-xs text-gray-600">
                        <p>Processed: {agent.processed} items</p>
                        <p>Last active: {agent.lastActive}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <Button variant="outline" size="sm" className="w-full mt-4">
                  Manage Agents
                </Button>
              </Card>
            </div>
          </div>
        </>
      )}

      {/* Requests Tab */}
      {selectedTab === "requests" && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-medium text-gray-900">All Requests</h2>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                Filter
              </Button>
              <Button variant="outline" size="sm">
                Export
              </Button>
            </div>
          </div>

          {requestsLoading ? (
            <Loading />
          ) : (
            <div className="space-y-4">
              {requests?.map((request) => (
                <div
                  key={request.id}
                  className="border border-gray-200 rounded-lg p-4"
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
                        <span className="text-xs text-gray-500">
                          ID: {request.id.slice(0, 8)}
                        </span>
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
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Button variant="outline" size="sm">
                        <EyeIcon className="w-4 h-4" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <PencilIcon className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                      >
                        <TrashIcon className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Resources Tab */}
      {selectedTab === "resources" && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-medium text-gray-900">
              Resource Management
            </h2>
            <Button>Add Resource</Button>
          </div>

          {resourcesLoading ? (
            <Loading />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resources?.map((resource) => (
                <div
                  key={resource.id}
                  className="border border-gray-200 rounded-lg p-4"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-gray-900">
                      {resource.name}
                    </h3>
                    <Badge
                      color={
                        resource.current_stock < resource.low_stock_threshold
                          ? "red"
                          : "green"
                      }
                    >
                      {resource.current_stock < resource.low_stock_threshold
                        ? "Low Stock"
                        : "In Stock"}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {resource.description}
                  </p>
                  <div className="text-sm text-gray-500">
                    <p>
                      Stock: {resource.current_stock} / {resource.max_capacity}
                    </p>
                    <p>Location: {resource.location}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Users Tab */}
      {selectedTab === "users" && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-medium text-gray-900">
              User Management
            </h2>
            <Button>Add User</Button>
          </div>
          <div className="text-center py-8">
            <UserGroupIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">
              User management interface coming soon...
            </p>
          </div>
        </Card>
      )}
    </DashboardLayout>
  );
};
