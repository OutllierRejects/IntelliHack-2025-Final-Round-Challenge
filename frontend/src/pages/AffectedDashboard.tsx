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
        return 'primary';
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
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
            <Typography 
              variant="h4" 
              component="h1" 
              sx={{ 
                color: 'primary.contrastText',
                fontWeight: 'bold'
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
                  boxShadow: 3
                },
                transition: 'all 0.2s',
                borderRadius: 2
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
                        label={request.status.replace('_', ' ')}
                        color={getStatusColor(request.status) as any}
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
                      {request.description}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color="text.secondary"
                      sx={{ display: 'flex', alignItems: 'center' }}
                    >
                      <MapPinIcon className="h-4 w-4 inline-block mr-1 text-primary-main" />
                      {request.location}
                    </Typography>
                  </CardContent>
                  <Divider />
                  <CardActions sx={{ p: 2, bgcolor: 'background.default' }}>
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
                  </CardActions>
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
                bgcolor: 'background.paper'
              }
            }}
          >
            <DialogTitle sx={{ 
              bgcolor: 'primary.main', 
              color: 'primary.contrastText',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
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
                          borderColor: 'primary.dark',
                          bgcolor: 'primary.light',
                          color: 'primary.dark'
                        },
                        borderRadius: 2
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
                      bgcolor: 'secondary.dark'
                    },
                    borderRadius: 2
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