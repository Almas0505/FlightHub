# Contributing to FlightHub

First off, thank you for considering contributing to FlightHub! 🎉

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When creating a bug report, include:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected
- **Include screenshots** if relevant
- **Include your environment details** (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any relevant examples** from other projects

### Pull Requests

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes** following our coding standards

3. **Test your changes**:
   ```bash
   # Backend tests
   pytest tests/ -v
   
   # Frontend tests
   cd frontend && npm run test
   ```

4. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add amazing feature"
   ```
   
   Commit types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting)
   - `refactor`: Code refactoring
   - `test`: Adding tests
   - `chore`: Maintenance tasks

5. **Push to your fork** and submit a pull request

6. **Wait for review** - we'll review your PR as soon as possible!

## Development Setup

### Prerequisites

- Docker Desktop
- Python 3.11+
- Node.js 20+
- Git

### Local Development

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/flighthub.git
   cd flighthub
   ```

2. **Start infrastructure**:
   ```bash
   docker-compose up -d postgres mongodb redis rabbitmq
   ```

3. **Backend development** (example with Flight Search):
   ```bash
   cd flight-search-service
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8001
   ```

4. **Frontend development**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Coding Standards

### Python

- Follow **PEP 8** style guide
- Use **type hints** for function signatures
- Format code with **Black**: `black .`
- Sort imports with **isort**: `isort .`
- Lint with **flake8**: `flake8 .`
- Document functions with docstrings

Example:
```python
from typing import List, Optional

async def search_flights(
    origin: str,
    destination: str,
    date: str,
    passengers: int = 1
) -> List[Flight]:
    """
    Search for available flights.
    
    Args:
        origin: IATA code of departure airport
        destination: IATA code of arrival airport
        date: Departure date in YYYY-MM-DD format
        passengers: Number of passengers (default: 1)
    
    Returns:
        List of available flights
    """
    # Implementation
    pass
```

### TypeScript/React

- Follow **Airbnb JavaScript Style Guide**
- Use **functional components** with hooks
- Format code with **Prettier**
- Use **TypeScript** for type safety
- Name components with **PascalCase**
- Name files with **kebab-case** for utilities, **PascalCase** for components

Example:
```typescript
interface FlightSearchProps {
  onSearch: (params: SearchParams) => void;
  loading: boolean;
}

export const FlightSearch: React.FC<FlightSearchProps> = ({ 
  onSearch, 
  loading 
}) => {
  // Implementation
  return <div>...</div>;
};
```

### Docker

- Use **multi-stage builds** for optimization
- Include health checks in Dockerfiles
- Minimize layer count
- Use specific base image versions (no `latest`)
- Clean up temporary files in same RUN command

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_search.py -v
```

### Frontend Tests

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### Integration Tests

```bash
# Start all services
docker-compose up -d

# Run E2E tests
pytest tests/integration/ -v
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update API documentation if you add/modify endpoints
- Include code examples in documentation

## Project Structure

```
flighthub/
├── .github/workflows/       # CI/CD pipelines
├── flighthub-api-gateway/  # API Gateway service
├── user-service/           # User management
├── flight-search-service/  # Flight search
├── booking-service/        # Booking management
├── payment-service/        # Payment processing
├── notification-service/   # Notifications
├── frontend/               # React frontend
└── docker-compose.yml      # Service orchestration
```

## Need Help?

- 📚 Check the [README.md](README.md)
- 💬 Open an issue for questions
- 📧 Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to FlightHub!** 🚀✈️
