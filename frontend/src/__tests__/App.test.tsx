import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

// Mock the WebSocket provider
vi.mock('../components/providers/WebSocketProvider', () => ({
  WebSocketProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>
}))

// Mock the auth store
vi.mock('../store', () => ({
  useAuthStore: () => ({
    user: null,
    isAuthenticated: false,
    login: vi.fn(),
    logout: vi.fn(),
    initializeAuth: vi.fn()
  })
}))

const renderApp = () => {
  return render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  )
}

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders without crashing', () => {
    renderApp()
    expect(document.body).toBeTruthy()
  })

  it('shows navigation when app loads', () => {
    renderApp()
    // Check for navigation elements
    expect(screen.getByRole('navigation')).toBeInTheDocument()
  })

  it('handles authentication state correctly', async () => {
    renderApp()
    
    // Should show login/register options when not authenticated
    await waitFor(() => {
      expect(screen.getByText(/Login/i) || screen.getByText(/Sign In/i)).toBeInTheDocument()
    })
  })
})
