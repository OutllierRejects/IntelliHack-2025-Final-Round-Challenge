import React from 'react';
import { useAuthStore } from '../store';
import { AffectedIndividualDashboard } from '../components/dashboards/AffectedIndividualDashboard';
import { VolunteerDashboard } from '../components/dashboards/VolunteerDashboard';
import { FirstResponderDashboard } from '../components/dashboards/FirstResponderDashboard';
import { AdminDashboard } from '../components/dashboards/AdminDashboard';

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Please log in to access your dashboard
          </h2>
        </div>
      </div>
    );
  }

  const renderDashboard = () => {
    switch (user.role) {
      case 'affected_individual':
        return <AffectedIndividualDashboard />;
      case 'volunteer':
        return <VolunteerDashboard />;
      case 'first_responder':
        return <FirstResponderDashboard />;
      case 'admin':
        return <AdminDashboard />;
      default:
        return (
          <div className="min-h-screen flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Invalid user role
              </h2>
              <p className="text-gray-600">
                Please contact support for assistance.
              </p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderDashboard()}
    </div>
  );
};
