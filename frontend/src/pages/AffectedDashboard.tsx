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
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  CircularProgress,
  Paper,
  Divider,
  Chip,
  IconButton,
  Tooltip,
  ThemeProvider,
  createTheme
} from '@mui/material';
import {
  PlusIcon,
  MapPinIcon,
  DocumentTextIcon,
  PhotoIcon,
  XMarkIcon,
  CalendarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

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

interface HelpRequest {
  id: string;
  title: string;
  description: string;
  location: string;
  status: 'pending' | 'in_progress' | 'completed';
  image_url?: string;
  created_at: string;
}

export default function AffectedDashboard() {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const { data: helpRequests, isLoading } = useQuery<HelpRequest[]>({
    queryKey: ['helpRequests'],
    queryFn: () => apiClient.get('/help-requests').then(res => res.data)
  });

  const createHelpRequest = useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await apiClient.post('/help-requests', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['helpRequests'] });
      handleClose();
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Failed to create help request');
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('location', location);
    if (image) {
      formData.append('image', image);
    }

    createHelpRequest.mutate(formData);
  };

  const handleClose = () => {
    setOpen(false);
    setTitle('');
    setDescription('');
    setLocation('');
    setImage(null);
    setError('');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'warning';
      case 'in_progress':
        return 'default';
      case 'completed':
        return 'success';
      default:
        return 'default';
    }
  };

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
          <Box 
            display="flex" 
            justifyContent="space-between" 
            alignItems="center" 
            mb={4}
            sx={{
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              backdropFilter: 'blur(10px)',
              borderRadius: 3,
              p: 3,
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
            }}
          >
            <Typography 
              variant="h4" 
              component="h1" 
              sx={{ 
                color: 'primary.contrastText',
                fontWeight: 'bold',
                textShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
              }}
            >
              My Help Requests
            </Typography>
            <Button
              variant="contained"
              startIcon={<PlusIcon className="h-5 w-5" />}
              onClick={() => setOpen(true)}
              sx={{
                bgcolor: 'secondary.main',
                color: 'secondary.contrastText',
                '&:hover': {
                  bgcolor: 'secondary.dark',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 4px 8px rgba(100, 255, 218, 0.3)'
                },
                transition: 'all 0.2s',
                borderRadius: 2,
                px: 3
              }}
            >
              New Request
            </Button>
          </Box>

          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 3,
                borderRadius: 2,
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                '& .MuiAlert-icon': {
                  color: 'error.main'
                }
              }}
            >
              {error}
            </Alert>
          )}

          <Grid container spacing={3}>
            {helpRequests?.map((request) => (
              <Grid item xs={12} md={6} lg={4} key={request.id}>
                <Card 
                  sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: '0 12px 24px rgba(0, 0, 0, 0.15)'
                    },
                    border: '1px solid',
                    borderColor: 'primary.light',
                    borderRadius: 4,
                    overflow: 'hidden',
                    backgroundColor: 'rgba(255, 255, 255, 0.98)',
                    backdropFilter: 'blur(10px)',
                    position: 'relative'
                  }}
                >
                  {request.image_url && (
                    <Box
                      component="img"
                      src={request.image_url}
                      alt={request.title}
                      sx={{
                        height: 240,
                        objectFit: 'cover',
                        width: '100%',
                        borderBottom: '1px solid',
                        borderColor: 'primary.light',
                        transition: 'all 0.5s ease',
                        filter: 'brightness(0.95)',
                        '&:hover': {
                          transform: 'scale(1.02)',
                          filter: 'brightness(1.05)',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
                        }
                      }}
                    />
                  )}
                  <CardContent sx={{ 
                    flexGrow: 1, 
                    p: 3.5,
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 2.5
                  }}>
                    <Box display="flex" justifyContent="space-between" alignItems="flex-start" gap={2}>
                      <Typography 
                        variant="h6" 
                        component="h2" 
                        sx={{ 
                          color: 'primary.main',
                          fontWeight: 700,
                          fontSize: '1.25rem',
                          lineHeight: 1.4,
                          maxWidth: '70%',
                          letterSpacing: '0.01em'
                        }}
                      >
                        {request.title}
                      </Typography>
                      <Chip
                        label={request.status.replace('_', ' ')}
                        color={getStatusColor(request.status) as any}
                        size="small"
                        sx={{ 
                          fontWeight: 600,
                          fontSize: '0.75rem',
                          height: '28px',
                          '&.MuiChip-colorPrimary': {
                            bgcolor: '#ffffff',
                            color: '#000000',
                            border: '1px solid #e0e0e0',
                            '&:hover': {
                              bgcolor: '#f5f5f5'
                            }
                          },
                          '&.MuiChip-colorWarning': {
                            bgcolor: '#fff3e0',
                            color: '#e65100',
                            '&:hover': {
                              bgcolor: '#ffe0b2'
                            }
                          },
                          '&.MuiChip-colorSuccess': {
                            bgcolor: '#e8f5e9',
                            color: '#2e7d32',
                            '&:hover': {
                              bgcolor: '#c8e6c9'
                            }
                          }
                        }}
                      />
                    </Box>
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ 
                        lineHeight: 1.7,
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: 1.5,
                        flex: 1,
                        fontSize: '0.95rem',
                        color: 'text.primary',
                        opacity: 0.9
                      }}
                    >
                      <DocumentTextIcon className="h-5 w-5 mt-0.5 flex-shrink-0 text-primary-main" />
                      {request.description}
                    </Typography>
                    <Box sx={{ 
                      display: 'flex', 
                      flexDirection: 'column',
                      gap: 1.5,
                      mt: 'auto'
                    }}>
                      <Box sx={{ 
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                        backgroundColor: 'rgba(0, 0, 0, 0.02)',
                        p: 1.5,
                        borderRadius: 2,
                        border: '1px solid',
                        borderColor: 'primary.light',
                        transition: 'all 0.2s ease',
                        '&:hover': {
                          backgroundColor: 'rgba(0, 0, 0, 0.04)',
                          transform: 'translateX(4px)'
                        }
                      }}>
                        <MapPinIcon className="h-5 w-5 flex-shrink-0 text-primary-main" />
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: 'text.primary',
                            fontWeight: 500,
                            fontSize: '0.95rem'
                          }}
                        >
                          {request.location}
                        </Typography>
                      </Box>
                      <Box sx={{ 
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1,
                        opacity: 0.8
                      }}>
                        <CalendarIcon className="h-4 w-4 text-primary-main" />
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            color: 'text.secondary',
                            fontSize: '0.85rem',
                            fontWeight: 500
                          }}
                        >
                          {new Date(request.created_at).toLocaleDateString()}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Dialog 
            open={open} 
            onClose={handleClose} 
            maxWidth="sm" 
            fullWidth
            PaperProps={{
              sx: {
                borderRadius: 3,
                bgcolor: 'background.paper',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)'
              }
            }}
          >
            <DialogTitle sx={{ 
              bgcolor: 'primary.main', 
              color: 'primary.contrastText',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              py: 2
            }}>
              Create New Help Request
              <IconButton
                aria-label="close"
                onClick={handleClose}
                sx={{ 
                  color: 'primary.contrastText',
                  '&:hover': {
                    bgcolor: 'primary.dark'
                  }
                }}
              >
                <XMarkIcon className="h-5 w-5" />
              </IconButton>
            </DialogTitle>
            <form onSubmit={handleSubmit}>
              <DialogContent sx={{ pt: 3 }}>
                <TextField
                  autoFocus
                  margin="dense"
                  label="Title"
                  fullWidth
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                  sx={{ mb: 2 }}
                />
                <TextField
                  margin="dense"
                  label="Description"
                  fullWidth
                  multiline
                  rows={4}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  sx={{ mb: 2 }}
                />
                <TextField
                  margin="dense"
                  label="Location"
                  fullWidth
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  required
                  sx={{ mb: 2 }}
                />
                <Box mt={2}>
                  <input
                    accept="image/*"
                    type="file"
                    id="image-upload"
                    style={{ display: 'none' }}
                    onChange={(e) => setImage(e.target.files?.[0] || null)}
                  />
                  <label htmlFor="image-upload">
                    <Button
                      variant="outlined"
                      component="span"
                      startIcon={<PhotoIcon className="h-5 w-5" />}
                      fullWidth
                      sx={{
                        borderColor: 'primary.main',
                        color: 'primary.main',
                        '&:hover': {
                          borderColor: '#e0e0e0',
                          bgcolor: '#e0e0e0',
                          color: '#424242'
                        },
                        borderRadius: 2,
                        py: 1.5
                      }}
                    >
                      {image ? 'Change Image' : 'Upload Image'}
                    </Button>
                  </label>
                  {image && (
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ mt: 1, textAlign: 'center' }}
                    >
                      Selected: {image.name}
                    </Typography>
                  )}
                </Box>
              </DialogContent>
              <DialogActions sx={{ p: 2, bgcolor: 'background.default' }}>
                <Button 
                  onClick={handleClose}
                  sx={{ 
                    color: 'text.secondary',
                    '&:hover': {
                      bgcolor: 'action.hover'
                    }
                  }}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={createHelpRequest.isPending}
                  sx={{
                    bgcolor: 'secondary.main',
                    color: 'secondary.contrastText',
                    '&:hover': {
                      bgcolor: 'secondary.dark',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 8px rgba(100, 255, 218, 0.3)'
                    },
                    transition: 'all 0.2s',
                    borderRadius: 2,
                    px: 3
                  }}
                >
                  {createHelpRequest.isPending ? 'Creating...' : 'Create Request'}
                </Button>
              </DialogActions>
            </form>
          </Dialog>
        </Container>
      </Box>
    </ThemeProvider>
  );
} 