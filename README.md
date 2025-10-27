# Multi-Tenant Notes API

A FastAPI-based multi-tenant notes application with role-based access control. Organizations can create users and manage notes with proper permission controls.

## Features

- Multi-tenant architecture with organization isolation
- Role-based permissions (reader, writer, admin)
- RESTful API with full CRUD operations
- Async database operations with MongoDB
- Docker containerization
- Automated testing with pytest

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB locally or use MongoDB Atlas

3. Run the application:
```bash
uvicorn main:app --reload
```

4. Access the API at `http://localhost:8000`

## API Endpoints

### Organizations
- `POST /organizations/` - Create organization
- `GET /organizations/` - List organizations

### Users
- `POST /organizations/{org_id}/users/` - Create user

### Notes
- `POST /notes/` - Create note (writer/admin only)
- `GET /notes/` - List notes (all roles)
- `GET /notes/{id}` - Get specific note (all roles)
- `DELETE /notes/{id}` - Delete note (admin only)

## Authentication

All requests require these headers:
- `X-Org-ID`: Organization ID
- `X-User-ID`: User ID

## User Roles

- **reader**: Can view notes
- **writer**: Can create and view notes
- **admin**: Can create, view, and delete notes

## Example Usage

Create an organization:
```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Blutech"}'
```

Create a user:
```bash
curl -X POST "http://localhost:8000/organizations/{org_id}/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Carkson", "email": "carkson@blutech.com", "role": "admin"}'
```

Create a note:
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org_id}" \
  -H "X-User-ID: {user_id}" \
  -d '{"title": "Meeting Notes", "content": "Discussed project updates"}'
```

## Testing

Run tests:
```bash
pytest
```

## Docker

Run with Docker Compose:
```bash
docker-compose up --build
```

## Documentation

- API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Project Structure

```
├── app/
│   ├── middleware/     # Auth middleware
│   ├── models/        # Pydantic models
│   ├── routers/       # API routes
│   ├── services/      # Business logic
│   └── database.py    # DB connection
├── tests/            # Test files
├── main.py          # App entry point
├── requirements.txt # Dependencies
└── Dockerfile      # Container config
```


## Example API Usage

### 1. Create Organization
```bash
curl -X POST "http://localhost:8000/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "blutech Corporation"}'
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "blutech Corporation",
  "created_at": "2025-01-25T10:30:00Z"
}
```

### 2. Create User
```bash
curl -X POST "http://localhost:8000/organizations/507f1f77bcf86cd799439011/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "David Carkson",
    "email": "David.Carkson@blutech.com",
    "role": "admin"
  }'
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "org_id": "507f1f77bcf86cd799439011",
  "name": "David Carkson",
  "email": "David.Carkson@blutech.com",
  "role": "admin",
  "created_at": "2025-01-25T10:30:00Z"
}
```

### 3. Create Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: 507f1f77bcf86cd799439011" \
  -H "X-User-ID: 507f1f77bcf86cd799439012" \
  -d '{
    "title": "Project Kickoff Meeting",
    "content": "Discussed project timeline, assigned tasks to team members, set up initial sprint planning."
  }'
```

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439013",
  "org_id": "507f1f77bcf86cd799439011",
  "title": "Project Kickoff Meeting",
  "content": "Discussed project timeline, assigned tasks to team members, set up initial sprint planning.",
  "created_by": "507f1f77bcf86cd799439012",
  "created_at": "2025-01-25T10:30:00Z",
  "updated_at": "2025-01-25T10:30:00Z"
}
```

### 4. List Notes
```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "X-Org-ID: 507f1f77bcf86cd799439011" \
  -H "X-User-ID: 507f1f77bcf86cd799439012"
```

### 5. Delete Note (Admin Only)
```bash
curl -X DELETE "http://localhost:8000/notes/507f1f77bcf86cd799439013" \
  -H "X-Org-ID: 507f1f77bcf86cd799439011" \
  -H "X-User-ID: 507f1f77bcf86cd799439012"
```

## Testing

### Run Test Suite
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_notes.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Structure
- **Unit Tests**: Service layer business logic
- **Integration Tests**: Full API endpoint testing with httpx
- **Authentication Tests**: Permission and access control validation

## Docker Commands

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build --no-deps app
```

## Configuration

### Environment Variables
```bash
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=notes_api

# Optional: Custom host/port
HOST=0.0.0.0
PORT=8000
```

### Database Collections
- `organizations`: Organization/tenant data
- `users`: User accounts with role assignments
- `notes`: Notes with organization isolation

## Security Features

- **Tenant Isolation**: Complete data separation between organizations
- **Role-Based Access**: Granular permissions per user role
- **Input Validation**: Pydantic model validation on all inputs
- **Error Handling**: Secure error responses without data leakage
- **Authentication Middleware**: Centralized auth validation

## Data Models

### Organization
```python
{
  "_id": "ObjectId",
  "name": "string",
  "created_at": "datetime"
}
```

### User
```python
{
  "_id": "ObjectId",
  "org_id": "string",
  "name": "string",
  "email": "string",
  "role": "reader|writer|admin",
  "created_at": "datetime"
}
```

### Note
```python
{
  "_id": "ObjectId",
  "org_id": "string",
  "title": "string",
  "content": "string",
  "created_by": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Deployment

### Production Deployment
1. Set environment variables for production database
2. Use `docker-compose.prod.yml` for production configuration
3. Configure reverse proxy (nginx) for SSL termination
4. Set up monitoring and logging

### Scaling Considerations
- **Horizontal Scaling**: Stateless API design supports multiple instances
- **Database Sharding**: MongoDB sharding by organization for large scale
- **Caching**: Redis for session and response caching
- **Load Balancing**: Distribute requests across multiple API instances

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
- Check the API documentation at `/docs`
- Review the test suite for usage examples
- Create an issue in the repository

---

**Built with**: FastAPI, MongoDB, Pydantic, Docker
**Tested with**: pytest, httpx, MongoDB
**Deployed via**: Docker Compose, Container orchestration