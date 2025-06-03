import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { requestService } from '../../services';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { Select } from '../ui/Select';
import { Loading } from '../ui/Loading';
import { RequestType, Priority } from '../../types';

interface CreateRequestFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export const CreateRequestForm: React.FC<CreateRequestFormProps> = ({
  onSuccess,
  onCancel,
}) => {
  const [formData, setFormData] = useState({
    request_type: '' as RequestType,
    description: '',
    location: '',
    urgency_level: '' as Priority,
    people_count: '',
    contact_info: '',
    specific_needs: '',
  });

  const createRequestMutation = useMutation({
    mutationFn: requestService.createRequest,
    onSuccess: () => {
      onSuccess();
    },
    onError: (error: any) => {
      console.error('Failed to create request:', error);
      // TODO: Show error toast
    },
  });

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const requestData = {
      ...formData,
      people_count: formData.people_count ? parseInt(formData.people_count) : undefined,
      urgency_level: formData.urgency_level as Priority,
      request_type: formData.request_type as RequestType,
    };

    createRequestMutation.mutate(requestData);
  };

  const requestTypeOptions = [
    { value: 'medical_emergency', label: 'Medical Emergency' },
    { value: 'shelter', label: 'Shelter Needed' },
    { value: 'food_water', label: 'Food & Water' },
    { value: 'rescue', label: 'Search & Rescue' },
    { value: 'transportation', label: 'Transportation' },
    { value: 'security', label: 'Security' },
    { value: 'utilities', label: 'Utilities' },
    { value: 'other', label: 'Other' },
  ];

  const priorityOptions = [
    { value: 'low', label: 'Low - Non-urgent' },
    { value: 'medium', label: 'Medium - Important' },
    { value: 'high', label: 'High - Urgent' },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="request_type" className="block text-sm font-medium text-gray-700 mb-2">
            Type of Help Needed *
          </label>
          <Select
            value={formData.request_type}
            onChange={(value) => handleInputChange('request_type', value)}
            options={requestTypeOptions}
            placeholder="Select request type"
            required
          />
        </div>

        <div>
          <label htmlFor="urgency_level" className="block text-sm font-medium text-gray-700 mb-2">
            Urgency Level *
          </label>
          <Select
            value={formData.urgency_level}
            onChange={(value) => handleInputChange('urgency_level', value)}
            options={priorityOptions}
            placeholder="Select urgency level"
            required
          />
        </div>

        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
            Location *
          </label>
          <Input
            id="location"
            type="text"
            value={formData.location}
            onChange={(e) => handleInputChange('location', e.target.value)}
            placeholder="Enter specific location or address"
            required
          />
        </div>

        <div>
          <label htmlFor="people_count" className="block text-sm font-medium text-gray-700 mb-2">
            Number of People Affected
          </label>
          <Input
            id="people_count"
            type="number"
            value={formData.people_count}
            onChange={(e) => handleInputChange('people_count', e.target.value)}
            placeholder="How many people need help?"
            min="1"
          />
        </div>

        <div className="md:col-span-2">
          <label htmlFor="contact_info" className="block text-sm font-medium text-gray-700 mb-2">
            Contact Information *
          </label>
          <Input
            id="contact_info"
            type="text"
            value={formData.contact_info}
            onChange={(e) => handleInputChange('contact_info', e.target.value)}
            placeholder="Phone number or other contact method"
            required
          />
        </div>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Description of Situation *
        </label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => handleInputChange('description', e.target.value)}
          placeholder="Please describe your situation in detail..."
          rows={4}
          required
        />
      </div>

      <div>
        <label htmlFor="specific_needs" className="block text-sm font-medium text-gray-700 mb-2">
          Specific Needs or Resources Required
        </label>
        <Textarea
          id="specific_needs"
          value={formData.specific_needs}
          onChange={(e) => handleInputChange('specific_needs', e.target.value)}
          placeholder="List any specific resources, equipment, or assistance needed..."
          rows={3}
        />
      </div>

      {/* Emergency Warning */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Life-Threatening Emergency?
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>
                If this is a life-threatening emergency, please call <strong>911</strong> immediately.
                This system is for coordination of disaster response and may not provide immediate assistance.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-end space-x-4">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={createRequestMutation.isPending}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={createRequestMutation.isPending || !formData.request_type || !formData.description || !formData.location || !formData.urgency_level || !formData.contact_info}
          className="bg-red-600 hover:bg-red-700 text-white"
        >
          {createRequestMutation.isPending ? (
            <Loading size="sm" className="text-white" />
          ) : (
            'Submit Request'
          )}
        </Button>
      </div>

      {createRequestMutation.isError && (
        <div className="text-red-600 text-sm">
          Failed to submit request. Please try again.
        </div>
      )}
    </form>
  );
};
