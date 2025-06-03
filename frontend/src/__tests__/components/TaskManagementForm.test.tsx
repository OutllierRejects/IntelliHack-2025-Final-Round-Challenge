import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import TaskManagementForm from '../../components/forms/TaskManagementForm'

// Mock the API service
vi.mock('../../services/api', () => ({
  api: {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

describe('TaskManagementForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders form fields correctly', () => {
    render(
      <TaskManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/priority/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/assigned to/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/due date/i)).toBeInTheDocument()
  })

  it('handles form submission correctly', async () => {
    render(
      <TaskManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Test Task' }
    })
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'Test Description' }
    })
    fireEvent.change(screen.getByLabelText(/priority/i), {
      target: { value: 'HIGH' }
    })

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'Test Task',
        description: 'Test Description',
        priority: 'HIGH',
        assigned_to: '',
        due_date: ''
      })
    })
  })

  it('validates required fields', async () => {
    render(
      <TaskManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Try to submit without filling required fields
    fireEvent.click(screen.getByRole('button', { name: /create task/i }))

    await waitFor(() => {
      expect(screen.getByText(/title is required/i)).toBeInTheDocument()
    })

    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it('handles cancel action', () => {
    render(
      <TaskManagementForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))
    expect(mockOnCancel).toHaveBeenCalled()
  })

  it('populates form when editing existing task', () => {
    const existingTask = {
      id: '1',
      title: 'Existing Task',
      description: 'Existing Description',
      priority: 'MEDIUM',
      assigned_to: 'user@example.com',
      due_date: '2024-12-31'
    }

    render(
      <TaskManagementForm
        task={existingTask}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    expect(screen.getByDisplayValue('Existing Task')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Existing Description')).toBeInTheDocument()
    expect(screen.getByDisplayValue('MEDIUM')).toBeInTheDocument()
  })
})
