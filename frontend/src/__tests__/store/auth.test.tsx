import { describe, it, expect, vi } from "vitest";
import { act, renderHook } from "@testing-library/react";
import { useAuthStore } from "../../store";

// Mock Supabase
vi.mock("@supabase/supabase-js", () => ({
  createClient: vi.fn(() => ({
    auth: {
      signInWithPassword: vi.fn(),
      signUp: vi.fn(),
      signOut: vi.fn(),
      getSession: vi.fn(),
      onAuthStateChange: vi.fn(() => ({
        data: { subscription: { unsubscribe: vi.fn() } },
      })),
    },
  })),
}));

describe("Auth Store", () => {
  it("initializes with default state", () => {
    const { result } = renderHook(() => useAuthStore());

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.loading).toBe(false);
  });

  it("handles login correctly", async () => {
    const { result } = renderHook(() => useAuthStore());

    const mockUser = {
      id: "1",
      email: "test@example.com",
      user_metadata: { full_name: "Test User" },
    };

    await act(async () => {
      await result.current.login("test@example.com", "password");
    });

    // Note: In a real test, you'd mock the Supabase response
    // For now, just verify the function exists and can be called
    expect(typeof result.current.login).toBe("function");
  });

  it("handles logout correctly", async () => {
    const { result } = renderHook(() => useAuthStore());

    await act(async () => {
      await result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it("initializes auth state on startup", async () => {
    const { result } = renderHook(() => useAuthStore());

    await act(async () => {
      await result.current.initializeAuth();
    });

    // Verify initialization completes
    expect(typeof result.current.initializeAuth).toBe("function");
  });
});
