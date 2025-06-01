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
  ClipboardDocumentListIcon
} from '@heroicons/react/24/outline';

// Our app's color scheme and styling
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

// What a task looks like in our system
interface Task {
  id: string;
  help_request: {
    id: string;
    title: string;
    description: string;
    location: string;
    image_url?: string;
  };
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
}

export default function VolunteerDashboard() {
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  // Grab all tasks assigned to this volunteer
  const { data: tasks, isLoading } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: () => apiClient.get('/tasks').then(res => res.data)
  });

  // Update a task's status (start/complete)
  const updateTaskStatus = useMutation({
    mutationFn: async ({ taskId, status }: { taskId: string; status: string }) => {
      const response = await apiClient.patch(`/tasks/${taskId}`, { status });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to update task status');
    }
  });

  // Match status to the right color
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

  // Show loading spinner while we fetch tasks
  if (isLoading) {
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
            My Tasks
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

          <Grid container spacing={3}>
            {!tasks?.length ? (
              <Grid item xs={12}>
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
                    No tasks available
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    You don't have any assigned tasks at the moment
                  </Typography>
                </Paper>
              </Grid>
            ) : (
              tasks.map((task) => (
                <Grid item xs={12} md={6} lg={4} key={task.id}>
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
                    {task.help_request.image_url && (
                      <Box
                        component="img"
                        src={task.help_request.image_url}
                        alt={task.help_request.title}
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
                          {task.help_request.title}
                        </Typography>
                        <Chip
                          icon={getStatusIcon(task.status)}
                          label={task.status.replace('_', ' ')}
                          color={getStatusColor(task.status) as any}
                          size="small"
                          sx={{ 
                            fontWeight: 'medium',
                            '&.MuiChip-colorPrimary': {
                              bgcolor: 'primary.light',
                              color: 'primary.dark'
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
                        {task.help_request.description}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center' }}
                      >
                        <MapPinIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                        {task.help_request.location}
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
                          {new Date(task.created_at).toLocaleDateString()}
                        </Typography>
                      </Box>
                      <Box sx={{ flexGrow: 1 }} />
                      {task.status === 'pending' && (
                        <Button
                          variant="contained"
                          size="small"
                          onClick={() => updateTaskStatus.mutate({ taskId: task.id, status: 'in_progress' })}
                          sx={{
                            bgcolor: 'secondary.main',
                            color: 'secondary.contrastText',
                            '&:hover': {
                              bgcolor: 'secondary.dark'
                            },
                            borderRadius: 2
                          }}
                        >
                          Start Task
                        </Button>
                      )}
                      {task.status === 'in_progress' && (
                        <Button
                          variant="contained"
                          size="small"
                          onClick={() => updateTaskStatus.mutate({ taskId: task.id, status: 'completed' })}
                          sx={{
                            bgcolor: 'secondary.main',
                            color: 'secondary.contrastText',
                            '&:hover': {
                              bgcolor: 'secondary.dark'
                            },
                            borderRadius: 2
                          }}
                        >
                          Complete Task
                        </Button>
                      )}
                    </CardActions>
                  </Card>
                </Grid>
              ))
            )}
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
} 