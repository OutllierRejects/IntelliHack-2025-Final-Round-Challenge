import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card } from '../ui/Card';
import { useCreateResource, useUpdateResource } from '../../hooks/api';
import { Resource } from '../../types';

const resourceSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  type: z.enum(['medical', 'food', 'shelter', 'clothing', 'equipment', 'transport', 'other']),
  quantity: z.number().min(0, 'Quantity must be positive'),
  unit: z.string().min(1, 'Unit is required'),
  location: z.string().min(1, 'Location is required'),
  description: z.string().optional(),
  minimumStock: z.number().min(0, 'Minimum stock must be positive').optional(),
});

type ResourceForm = z.infer<typeof resourceSchema>;

interface ResourceManagementFormProps {
  resource?: Resource;
  onClose: () => void;
}

export const ResourceManagementForm: React.FC<ResourceManagementFormProps> = ({
  resource,
  onClose,
}) => {
  const isEditing = !!resource;
  
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResourceForm>({
    resolver: zodResolver(resourceSchema),
    defaultValues: resource ? {
      name: resource.name,
      type: resource.type,
      quantity: resource.quantity,
      unit: resource.unit,
      location: resource.location,
      description: resource.description || '',
      minimumStock: resource.minimumStock || 0,
    } : {
      name: '',
      type: 'other',
      quantity: 0,
      unit: '',
      location: '',
      description: '',
      minimumStock: 0,
    },
  });

  const createResourceMutation = useCreateResource();
  const updateResourceMutation = useUpdateResource();

  const onSubmit = async (data: ResourceForm) => {
    try {
      if (isEditing && resource) {
        await updateResourceMutation.mutateAsync({
          id: resource.id,
          updates: data,
        });
      } else {
        await createResourceMutation.mutateAsync(data);
      }
      onClose();
    } catch (error) {
      console.error('Failed to save resource:', error);
    }
  };

  const resourceTypes = [
    { value: 'medical', label: 'Medical Supplies' },
    { value: 'food', label: 'Food & Water' },
    { value: 'shelter', label: 'Shelter Materials' },
    { value: 'clothing', label: 'Clothing' },
    { value: 'equipment', label: 'Equipment' },
    { value: 'transport', label: 'Transportation' },
    { value: 'other', label: 'Other' },
  ];

  return (
    <Card className="max-w-2xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          {isEditing ? 'Update Resource' : 'Add New Resource'}
        </h2>
        <p className="text-gray-600">
          {isEditing 
            ? 'Update resource information and stock levels' 
            : 'Register a new resource in the system'
          }
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Resource Name *
            </label>
            <Input
              {...register('name')}
              placeholder="e.g., First Aid Kit"
              error={errors.name?.message}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type *
            </label>
            <select
              {...register('type')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {resourceTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
            {errors.type && (
              <p className="mt-1 text-sm text-red-600">{errors.type.message}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity *
            </label>
            <Input
              type="number"
              min="0"
              step="1"
              {...register('quantity', { valueAsNumber: true })}
              placeholder="0"
              error={errors.quantity?.message}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Unit *
            </label>
            <Input
              {...register('unit')}
              placeholder="e.g., boxes, liters, pieces"
              error={errors.unit?.message}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Stock
            </label>
            <Input
              type="number"
              min="0"
              step="1"
              {...register('minimumStock', { valueAsNumber: true })}
              placeholder="0"
              error={errors.minimumStock?.message}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Location *
          </label>
          <Input
            {...register('location')}
            placeholder="e.g., Warehouse A, Room 101"
            error={errors.location?.message}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            {...register('description')}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Additional details about the resource..."
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
          )}
        </div>

        <div className="flex justify-end space-x-4">
          <Button
            type="button"
            variant="outline"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting}
            loading={isSubmitting}
          >
            {isEditing ? 'Update Resource' : 'Add Resource'}
          </Button>
        </div>
      </form>
    </Card>
  );
};
