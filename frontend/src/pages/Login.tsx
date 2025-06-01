import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { UserRole } from '../lib/supabase';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  SelectChangeEvent,
  ThemeProvider,
  createTheme,
  InputAdornment
} from '@mui/material';
import {
  EnvelopeIcon,
  LockClosedIcon,
  UserIcon,
  ArrowRightIcon
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

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('affected');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setError('');
      setLoading(true);
      await signIn(email, role);
      navigate(`/dashboard/${role}`);
    } catch (err) {
      setError('Failed to sign in. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = (event: SelectChangeEvent) => {
    setRole(event.target.value as UserRole);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box 
        sx={{ 
          minHeight: '100vh',
          bgcolor: 'background.default',
          display: 'flex',
          alignItems: 'center',
          py: 4,
          backgroundImage: 'linear-gradient(135deg, #0a192f 0%, #112240 100%)'
        }}
      >
        <Container maxWidth="sm">
          <Paper 
            elevation={3}
            sx={{ 
              p: 4,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              bgcolor: 'background.paper',
              borderRadius: 3,
              border: '1px solid',
              borderColor: 'primary.light',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
            }}
          >
            <Box 
              sx={{ 
                width: 48, 
                height: 48, 
                borderRadius: '50%', 
                bgcolor: 'primary.main',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                mb: 2,
                boxShadow: '0 4px 12px rgba(10, 25, 47, 0.2)'
              }}
            >
              <LockClosedIcon className="h-6 w-6 text-white" />
            </Box>

            <Typography 
              component="h1" 
              variant="h4" 
              sx={{ 
                mb: 3,
                color: 'primary.main',
                fontWeight: 'bold',
                textAlign: 'center'
              }}
            >
              Welcome Back
            </Typography>

            <Typography 
              variant="body1" 
              color="text.secondary" 
              sx={{ 
                mb: 4,
                textAlign: 'center'
              }}
            >
              Sign in to access your dashboard
            </Typography>

            <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
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

              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                sx={{ mb: 2 }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                    </InputAdornment>
                  ),
                }}
              />

              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                sx={{ mb: 2 }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockClosedIcon className="h-5 w-5 text-gray-400" />
                    </InputAdornment>
                  ),
                }}
              />

              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel id="role-label">Role</InputLabel>
                <Select
                  labelId="role-label"
                  id="role"
                  value={role}
                  label="Role"
                  onChange={handleRoleChange}
                  startAdornment={
                    <InputAdornment position="start">
                      <UserIcon className="h-5 w-5 text-gray-400" />
                    </InputAdornment>
                  }
                >
                  <MenuItem value="affected">Affected Individual</MenuItem>
                  <MenuItem value="volunteer">Volunteer</MenuItem>
                  <MenuItem value="responder">First Responder</MenuItem>
                  <MenuItem value="admin">Administrator</MenuItem>
                </Select>
              </FormControl>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                disabled={loading}
                sx={{
                  py: 1.5,
                  bgcolor: 'primary.main',
                  borderRadius: 2,
                  '&:hover': {
                    bgcolor: 'primary.dark',
                    transform: 'translateY(-2px)',
                    boxShadow: 3
                  },
                  transition: 'all 0.2s'
                }}
                endIcon={!loading && <ArrowRightIcon className="h-5 w-5" />}
              >
                {loading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  'Sign in'
                )}
              </Button>
            </Box>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
} 