import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store';
import { authService } from '../services';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Card } from '../components/ui/Card';
import { Loading } from '../components/ui/Loading';
import { UserRole } from '../types';

export const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    phone: '',
    role: '' as UserRole,
    skills: '',
    location: '',
  });

  const navigate = useNavigate();
  const { setUser, setToken } = useAuthStore();

  const registerMutation = useMutation({
    mutationFn: authService.register,
    onSuccess: (data) => {
      setUser(data.user);
      setToken(data.access_token);
      navigate('/dashboard');
    },
    onError: (error: any) => {
      console.error('Registration failed:', error);
      // TODO: Show error toast
    },
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      // TODO: Show error toast
      return;
    }

    if (formData.email && formData.password && formData.fullName && formData.role) {
      const { confirmPassword, ...registrationData } = formData;
      registerMutation.mutate(registrationData);
    }
  };

  const roleOptions = [
    { value: 'affected_individual', label: 'Affected Individual' },
    { value: 'volunteer', label: 'Volunteer' },
    { value: 'first_responder', label: 'First Responder' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl p-8 bg-white/10 backdrop-blur-lg border border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Join Our Response Network
          </h1>
          <p className="text-gray-300">
            Help us coordinate disaster response efforts
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-gray-300 mb-2">
                Full Name *
              </label>
              <Input
                id="fullName"
                type="text"
                value={formData.fullName}
                onChange={(e) => handleInputChange('fullName', e.target.value)}
                placeholder="Enter your full name"
                required
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address *
              </label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="Enter your email"
                required
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-2">
                Phone Number
              </label>
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="Enter your phone number"
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-300 mb-2">
                Role *
              </label>
              <Select
                value={formData.role}
                onChange={(value) => handleInputChange('role', value)}
                options={roleOptions}
                placeholder="Select your role"
                className="bg-white/10 border-white/20 text-white"
              />
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-300 mb-2">
                Location
              </label>
              <Input
                id="location"
                type="text"
                value={formData.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="City, State"
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="skills" className="block text-sm font-medium text-gray-300 mb-2">
                Skills/Expertise
              </label>
              <Input
                id="skills"
                type="text"
                value={formData.skills}
                onChange={(e) => handleInputChange('skills', e.target.value)}
                placeholder="e.g., Medical, Search & Rescue"
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password *
              </label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                placeholder="Enter password"
                required
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
                Confirm Password *
              </label>
              <Input
                id="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                placeholder="Confirm password"
                required
                className="bg-white/10 border-white/20 text-white placeholder-gray-400"
              />
            </div>
          </div>

          <Button
            type="submit"
            disabled={registerMutation.isPending || !formData.email || !formData.password || !formData.fullName || !formData.role}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            {registerMutation.isPending ? (
              <Loading size="sm" className="text-white" />
            ) : (
              'Create Account'
            )}
          </Button>

          {registerMutation.isError && (
            <div className="text-red-400 text-sm text-center">
              Registration failed. Please try again.
            </div>
          )}
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-300">
            Already have an account?{' '}
            <Link
              to="/login"
              className="text-blue-400 hover:text-blue-300 font-medium"
            >
              Sign in
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
};
