# Disaster Response Coordination Platform Frontend

A React TypeScript frontend for the disaster response coordination platform.

## Features

- Authentication with Supabase
- Role-based dashboards for different user types
- Help request submission with image upload
- Task management for volunteers and first responders
- System health monitoring for administrators

## Prerequisites

- Node.js 18 or later
- npm or pnpm
- Supabase account
- Backend API running on port 8000

## Setup

1. Install dependencies:
   ```bash
   npm install
   # or
   pnpm install
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   VITE_API_URL=http://localhost:8000/api/v1
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

## Project Structure

- `/src/components` - Reusable UI components
- `/src/contexts` - React contexts (auth, etc.)
- `/src/lib` - Utility functions and API clients
- `/src/pages` - Page components
- `/src/types` - TypeScript type definitions

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Authentication

The application uses Supabase for authentication. Users can sign up with different roles:
- Affected Individuals
- Volunteers
- First Responders
- Administrators

## API Integration

The frontend communicates with the backend through versioned REST APIs (`/api/v1/*`). All API requests include the Supabase JWT token for authentication.

## Image Upload

Images are uploaded to Supabase Storage using pre-signed URLs. The storage bucket should be configured with appropriate security rules.

## Data Polling

The application uses React Query for data fetching and polling. Dashboards automatically refresh their data at regular intervals.
