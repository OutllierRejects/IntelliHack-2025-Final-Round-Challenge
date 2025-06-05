import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../lib/api';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Divider,
  Chip,
  ThemeProvider,
  createTheme,
  Paper
} from '@mui/material';
import {
  MapPinIcon,
  DocumentTextIcon,
  CalendarIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationCircleIcon,
  UserGroupIcon,
  PhoneIcon,
  ChartBarIcon,
  UsersIcon,
  ClipboardDocumentListIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';

// Theme setup with our brand colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#0a192f',
      light: '#112240',
      dark: '#020c1b',
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#64ffda',
      light: '#9effff',
      dark: '#14cba8',
      contrastText: '#0a192f'
    },
    background: {
      default: '#f0f7ff',
      paper: '#ffffff'
    }
  },
  shape: {
    borderRadius: 12
  }
});

// Types for our data
interface Stats {
  total_requests: number;
  active_requests: number;
  total_volunteers: number;
  total_responders: number;
}

interface HelpRequest {
  id: string;
  title: string;
  description: string;
  location: string;
  status: 'pending' | 'in_progress' | 'completed';
  image_url?: string;
  created_at: string;
  affected_user: {
    name: string;
    phone: string;
  };
}

export default function AdminDashboard() {
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  // Fetch dashboard stats
  const { data: stats, isLoading: isLoadingStats } = useQuery<Stats>({
    queryKey: ['stats'],
    queryFn: () => apiClient.get('/admin/stats').then(res => res.data)
  });

  // Get all help requests
  const { data: helpRequests, isLoading: isLoadingRequests } = useQuery<HelpRequest[]>({
    queryKey: ['helpRequests'],
    queryFn: () => apiClient.get('/help-requests').then(res => res.data)
  });

  // Handle request status updates
  const updateRequestStatus = useMutation({
    mutationFn: async ({ requestId, status }: { requestId: string; status: string }) => {
      const response = await apiClient.patch(`/help-requests/${requestId}`, { status });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['helpRequests'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to update request status');
    }
  });

  // Helper to get the right color for each status
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'warning';
      case 'in_progress':
        return 'primary';
      case 'completed':
        return 'success';
      default:
        return 'default';
    }
  };

  // Pick the right icon for each status
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <ExclamationCircleIcon className="h-4 w-4" />;
      case 'in_progress':
        return <ClockIcon className="h-4 w-4" />;
      case 'completed':
        return <CheckCircleIcon className="h-4 w-4" />;
      default:
        return null;
    }
  };

  // Show loading spinner while data is being fetched
  if (isLoadingStats || isLoadingRequests) {
    return (
      <ThemeProvider theme={theme}>
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            minHeight: '100vh',
            bgcolor: 'background.default',
            backgroundImage: 'linear-gradient(135deg, #0a192f 0%, #112240 100%)'
          }}
        >
          <CircularProgress sx={{ color: 'primary.main' }} />
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ 
        bgcolor: 'background.default', 
        minHeight: '100vh', 
        py: 4,
        backgroundImage: 'linear-gradient(135deg, #0a192f 0%, #112240 100%)'
      }}>
        <Container maxWidth="lg">
          <Typography 
            variant="h4" 
            component="h1" 
            sx={{ 
              mb: 4,
              color: 'primary.contrastText',
              fontWeight: 'bold'
            }}
          >
            Admin Dashboard
          </Typography>

          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 3,
                borderRadius: 2,
                '& .MuiAlert-icon': {
                  color: 'error.main'
                }
              }}
            >
              {error}
            </Alert>
          )}

          {/* Stats cards showing key metrics */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card 
                sx={{ 
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  borderRadius: 3,
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)'
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ChartBarIcon className="h-6 w-6 mr-2" />
                    <Typography variant="h6" component="div">
                      Total Requests
                    </Typography>
                  </Box>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                    {stats?.total_requests || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card 
                sx={{ 
                  bgcolor: 'primary.light',
                  color: 'primary.contrastText',
                  borderRadius: 3,
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)'
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ClockIcon className="h-6 w-6 mr-2" />
                    <Typography variant="h6" component="div">
                      Active Requests
                    </Typography>
                  </Box>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                    {stats?.active_requests || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card 
                sx={{ 
                  bgcolor: 'secondary.main',
                  color: 'secondary.contrastText',
                  borderRadius: 3,
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)'
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <UsersIcon className="h-6 w-6 mr-2" />
                    <Typography variant="h6" component="div">
                      Volunteers
                    </Typography>
                  </Box>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                    {stats?.total_volunteers || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card 
                sx={{ 
                  bgcolor: 'secondary.dark',
                  color: 'secondary.contrastText',
                  borderRadius: 3,
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)'
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ShieldCheckIcon className="h-6 w-6 mr-2" />
                    <Typography variant="h6" component="div">
                      Responders
                    </Typography>
                  </Box>
                  <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                    {stats?.total_responders || 0}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Typography 
            variant="h5" 
            component="h2" 
            sx={{ 
              mb: 3,
              color: 'primary.contrastText',
              fontWeight: 'bold'
            }}
          >
            Recent Help Requests
          </Typography>

          {/* Show empty state if no requests */}
          {!helpRequests?.length ? (
            <Paper 
              elevation={0}
              sx={{ 
                p: 4, 
                textAlign: 'center',
                bgcolor: 'background.paper',
                border: '1px solid',
                borderColor: 'primary.light',
                borderRadius: 3
              }}
            >
              <ClipboardDocumentListIcon className="h-12 w-12 mx-auto mb-2 text-primary-main" />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No help requests available
              </Typography>
              <Typography variant="body2" color="text.secondary">
                There are currently no help requests in the system
              </Typography>
            </Paper>
          ) : (
            <Grid container spacing={3}>
              {helpRequests.map((request) => (
                <Grid item xs={12} md={6} lg={4} key={request.id}>
                  <Card 
                    sx={{ 
                      height: '100%', 
                      display: 'flex', 
                      flexDirection: 'column',
                      transition: 'transform 0.2s, box-shadow 0.2s',
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: 4
                      },
                      border: '1px solid',
                      borderColor: 'primary.light',
                      borderRadius: 3,
                      overflow: 'hidden'
                    }}
                  >
                    {request.image_url && (
                      <Box
                        component="img"
                        src={request.image_url}
                        alt={request.title}
                        sx={{
                          height: 200,
                          objectFit: 'cover',
                          width: '100%'
                        }}
                      />
                    )}
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                        <Typography 
                          variant="h6" 
                          component="h2" 
                          gutterBottom
                          sx={{ 
                            color: 'primary.main',
                            fontWeight: 'bold'
                          }}
                        >
                          {request.title}
                        </Typography>
                        <Chip
                          icon={getStatusIcon(request.status)}
                          label={request.status.replace('_', ' ')}
                          color={getStatusColor(request.status) as any}
                          size="small"
                          sx={{ 
                            fontWeight: 'medium',
                            '&.MuiChip-colorPrimary': {
                              bgcolor: '#ffffff',
                              color: '#000000',
                              border: '1px solid #e0e0e0'
                            }
                          }}
                        />
                      </Box>
                      <Typography 
                        variant="body2" 
                        color="text.secondary" 
                        paragraph
                        sx={{ mb: 2 }}
                      >
                        <DocumentTextIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                        {request.description}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', mb: 1 }}
                      >
                        <MapPinIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                        {request.location}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', mb: 1 }}
                      >
                        <UserGroupIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                        {request.affected_user.name}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center' }}
                      >
                        <PhoneIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                        {request.affected_user.phone}
                      </Typography>
                    </CardContent>
                    <Divider />
                    <CardActions sx={{ p: 2, bgcolor: 'background.default' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography 
                          variant="caption" 
                          color="text.secondary" 
                          sx={{ 
                            display: 'flex',
                            alignItems: 'center',
                            gap: 0.5
                          }}
                        >
                          <CalendarIcon className="h-4 w-4" />
                          {new Date(request.created_at).toLocaleDateString()}
                        </Typography>
                      </Box>
                      <Box sx={{ flexGrow: 1 }} />
                      {request.status === 'pending' && (
                        <Button
                          variant="contained"
                          size="small"
                          onClick={() => updateRequestStatus.mutate({ requestId: request.id, status: 'in_progress' })}
                          sx={{
                            bgcolor: 'secondary.main',
                            color: 'secondary.contrastText',
                            '&:hover': {
                              bgcolor: 'secondary.dark'
                            },
                            borderRadius: 2
                          }}
                        >
                          Start Response
                        </Button>
                      )}
                      {request.status === 'in_progress' && (
                        <Button
                          variant="contained"
                          size="small"
                          onClick={() => updateRequestStatus.mutate({ requestId: request.id, status: 'completed' })}
                          sx={{
                            bgcolor: 'secondary.main',
                            color: 'secondary.contrastText',
                            '&:hover': {
                              bgcolor: 'secondary.dark'
                            },
                            borderRadius: 2
                          }}
                        >
                          Complete Response
                        </Button>
                      )}
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
} 