# Contributing Guide

Welcome to the disaster response coordination web application project! This guide will help you get started with contributing to the codebase.

## Getting Started

### Prerequisites

Before contributing, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **Docker** and Docker Compose
- **Git**
- **VS Code** (recommended) with suggested extensions

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/your-username/disaster-response-app.git
   cd disaster-response-app
   ```

2. **Install Dependencies**

   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd ../backend
   pip install -r requirements.txt

   # AI Services
   cd ../ai_services
   pip install -r requirements.txt
   ```

3. **Environment Setup**

   ```bash
   # Copy environment templates
   cp frontend/.env.example frontend/.env
   cp backend/.env.example backend/.env
   cp ai_services/.env.example ai_services/.env
   ```

4. **Database Setup**

   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Start Development Servers**

   ```bash
   # Terminal 1: Frontend
   cd frontend && npm start

   # Terminal 2: Backend
   cd backend && uvicorn app.main:app --reload

   # Terminal 3: AI Services
   cd ai_services && python run_mcp_server.py
   ```

## Code Style and Standards

### Frontend (TypeScript/React)

We use the following tools for code quality:

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking

#### Code Style Rules

```typescript
// ✅ Good: Use descriptive names
const emergencyRequestForm = () => { ... };

// ❌ Bad: Generic names
const form = () => { ... };

// ✅ Good: Proper typing
interface EmergencyRequest {
  id: string;
  type: 'medical' | 'fire' | 'natural_disaster' | 'security';
  description: string;
  location: GeoLocation;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

// ✅ Good: Component structure
const EmergencyRequestCard: React.FC<{ request: EmergencyRequest }> = ({ request }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      {/* Component content */}
    </div>
  );
};
```

#### Component Guidelines

1. **Functional Components**: Use function components with hooks
2. **Props Interface**: Define interfaces for all component props
3. **Custom Hooks**: Extract reusable logic into custom hooks
4. **Error Boundaries**: Wrap components that might throw errors
5. **Accessibility**: Include proper ARIA labels and semantic HTML

### Backend (Python/FastAPI)

We follow PEP 8 and use the following tools:

- **Black**: Code formatting
- **Flake8**: Code linting
- **mypy**: Type checking
- **isort**: Import sorting

#### Code Style Rules

```python
# ✅ Good: Clear function signatures with type hints
async def create_emergency_request(
    request: EmergencyRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EmergencyRequest:
    """Create a new emergency request."""
    # Implementation here
    pass

# ✅ Good: Proper error handling
from app.core.exceptions import ValidationError

async def validate_request_data(data: dict) -> dict:
    try:
        # Validation logic
        return validated_data
    except ValueError as e:
        raise ValidationError(f"Invalid request data: {str(e)}")

# ✅ Good: Dependency injection
class EmergencyRequestService:
    def __init__(self, db: Session, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service

    async def process_request(self, request: EmergencyRequestCreate) -> EmergencyRequest:
        # Service implementation
        pass
```

#### API Guidelines

1. **RESTful Design**: Follow REST principles for API endpoints
2. **Response Models**: Use Pydantic models for all responses
3. **Error Handling**: Implement consistent error response format
4. **Authentication**: Secure endpoints with proper authentication
5. **Documentation**: Use docstrings and OpenAPI annotations

### AI Services (Python)

#### AI Code Guidelines

```python
# ✅ Good: Agent base class implementation
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return response."""
        pass

    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data before processing."""
        required_fields = self.get_required_fields()
        return all(field in input_data for field in required_fields)

# ✅ Good: MCP tool implementation
from mcp import Tool

class EmergencyResponseTool(Tool):
    """Tool for processing emergency responses."""

    name = "process_emergency_request"
    description = "Process and prioritize emergency requests"

    async def run(self, request_data: dict) -> dict:
        """Execute the emergency response processing."""
        # Tool implementation
        return {"status": "processed", "priority": "high"}
```

## Git Workflow

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

#### Examples

```bash
# Good commit messages
feat(auth): add JWT token refresh functionality
fix(websocket): resolve connection timeout issues
docs(api): update authentication endpoint documentation
test(agents): add unit tests for emergency agent
refactor(database): optimize query performance

# Bad commit messages
fix: bug fix
update code
changes
```

### Pull Request Process

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/emergency-request-ui
   ```

2. **Make Changes and Commit**

   ```bash
   git add .
   git commit -m "feat(ui): add emergency request form component"
   ```

3. **Push and Create PR**

   ```bash
   git push origin feature/emergency-request-ui
   ```

4. **PR Template**

   ```markdown
   ## Description

   Brief description of changes made.

   ## Type of Change

   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing

   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Checklist

   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No console errors or warnings
   ```

## Testing Requirements

### Before Submitting PR

1. **Run All Tests**

   ```bash
   # Frontend tests
   cd frontend && npm test

   # Backend tests
   cd backend && pytest

   # AI service tests
   cd ai_services && pytest
   ```

2. **Code Coverage**

   - Maintain minimum 80% code coverage
   - Add tests for new features
   - Update tests for modified functionality

3. **Manual Testing**
   - Test the specific feature/fix
   - Verify no regression in existing functionality
   - Test across different user roles

## Documentation Standards

### Code Documentation

1. **Function Documentation**

   ```python
   async def process_emergency_request(
       request: EmergencyRequestCreate,
       db: Session
   ) -> EmergencyRequest:
       """
       Process a new emergency request.

       Args:
           request: The emergency request data to process
           db: Database session for data persistence

       Returns:
           EmergencyRequest: The created emergency request object

       Raises:
           ValidationError: If request data is invalid
           DatabaseError: If database operation fails
       """
   ```

2. **Component Documentation**
   ```typescript
   /**
    * Emergency request form component for affected individuals.
    *
    * Allows users to submit emergency requests with location,
    * type, description, and priority information.
    *
    * @param onSubmit - Callback function called when form is submitted
    * @param initialData - Optional initial form data for editing
    */
   interface EmergencyRequestFormProps {
     onSubmit: (data: EmergencyRequestData) => void;
     initialData?: Partial<EmergencyRequestData>;
   }
   ```

### README Updates

When adding new features or making significant changes:

1. Update relevant README sections
2. Add/update setup instructions if needed
3. Update feature list and descriptions
4. Include new environment variables

## Code Review Guidelines

### For Authors

1. **Self-Review**: Review your own code before submitting
2. **Small PRs**: Keep PRs focused and reasonably sized
3. **Clear Description**: Explain what and why, not just how
4. **Testing**: Include relevant tests and manual testing notes

### For Reviewers

1. **Constructive Feedback**: Be helpful and specific
2. **Test the Changes**: Pull and test significant changes
3. **Ask Questions**: If something is unclear, ask for clarification
4. **Approve Thoughtfully**: Ensure code meets quality standards

## Issue Reporting

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**

- OS: [e.g. macOS, Windows, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 22]

**Additional Context**
Any other context about the problem.
```

### Feature Requests

Use this template for feature requests:

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
Describe how you envision this feature working.

**Alternative Solutions**
Any alternative approaches you've considered.

**Additional Context**
Any other context or screenshots about the feature request.
```

## Development Environment

### Recommended VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode.vscode-eslint",
    "ms-python.mypy-type-checker"
  ]
}
```

### Docker Development

For consistent development environment:

```bash
# Build and start all services
docker-compose up --build

# Start specific service
docker-compose up frontend

# Run tests in containers
docker-compose run frontend npm test
docker-compose run backend pytest
```

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. [ ] All tests pass
2. [ ] Documentation updated
3. [ ] CHANGELOG.md updated
4. [ ] Version numbers updated
5. [ ] Create release tag
6. [ ] Deploy to staging
7. [ ] Manual testing on staging
8. [ ] Deploy to production

## Getting Help

- **Documentation**: Check the `/docs` directory
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Create an issue for bugs or feature requests
- **Code Review**: Request review from maintainers

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to the disaster response coordination system! Your efforts help make emergency response more effective and save lives.
