import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import Login from './pages/Login';
import AffectedDashboard from './pages/AffectedDashboard';
import VolunteerDashboard from './pages/VolunteerDashboard';
import ResponderDashboard from './pages/ResponderDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Unauthorized from './pages/Unauthorized';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  console.log('App component rendering'); // Debug log

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/unauthorized" element={<Unauthorized />} />
              
              <Route
                path="/dashboard/affected"
                element={
                  <ProtectedRoute allowedRoles={['affected']}>
                    <AffectedDashboard />
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/dashboard/volunteer"
                element={
                  <ProtectedRoute allowedRoles={['volunteer']}>
                    <VolunteerDashboard />
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/dashboard/responder"
                element={
                  <ProtectedRoute allowedRoles={['responder']}>
                    <ResponderDashboard />
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/dashboard/admin"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />
              
              <Route path="/" element={<Login />} />
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
