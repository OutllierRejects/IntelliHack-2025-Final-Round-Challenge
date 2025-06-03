import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ResourceManagementForm from '../../components/forms/ResourceManagementForm'

describe('ResourceManagementForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders form fields correctly', () => {
    render(
      <ResourceManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/type/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/location/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/capacity/i)).toBeInTheDocument()
  })

  it('handles form submission correctly', async () => {
    render(
      <ResourceManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'Fire Truck #1' }
    })
    fireEvent.change(screen.getByLabelText(/type/i), {
      target: { value: 'FIRE_TRUCK' }
    })
    fireEvent.change(screen.getByLabelText(/status/i), {
      target: { value: 'AVAILABLE' }
    })
    fireEvent.change(screen.getByLabelText(/location/i), {
      target: { value: 'Station A' }
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /create resource/i }))

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        name: 'Fire Truck #1',
        type: 'FIRE_TRUCK',
        status: 'AVAILABLE',
        location: 'Station A',
        capacity: '',
        description: ''
      })
    })
  })

  it('validates required fields', async () => {
    render(
      <ResourceManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Try to submit without filling required fields
    fireEvent.click(screen.getByRole('button', { name: /create resource/i }))

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument()
    })

    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it('handles different resource types', () => {
    render(
      <ResourceManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    const typeSelect = screen.getByLabelText(/type/i)
    
    // Should include common resource types
    expect(screen.getByText('Fire Truck')).toBeInTheDocument()
    expect(screen.getByText('Ambulance')).toBeInTheDocument()
    expect(screen.getByText('Police Car')).toBeInTheDocument()
    expect(screen.getByText('Helicopter')).toBeInTheDocument()
  })

  it('populates form when editing existing resource', () => {
    const existingResource = {
      id: '1',
      name: 'Ambulance #2',
      type: 'AMBULANCE',
      status: 'BUSY',
      location: 'Hospital',
      capacity: '2',
      description: 'Advanced life support ambulance'
    }

    render(
      <ResourceManagementForm
        resource={existingResource}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    expect(screen.getByDisplayValue('Ambulance #2')).toBeInTheDocument()
    expect(screen.getByDisplayValue('AMBULANCE')).toBeInTheDocument()
    expect(screen.getByDisplayValue('BUSY')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Hospital')).toBeInTheDocument()
  })
})
