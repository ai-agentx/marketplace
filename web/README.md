# Agent Marketplace

A platform for registering, discovering, and executing AI agents compatible with OpenAI's agents framework.

## Project Structure

The project consists of two main components:

1. **Backend API** - Python FastAPI application that provides RESTful endpoints for managing agents and executions
2. **Frontend UI** - Vue.js application that provides a user interface for interacting with the API

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.11+ (for local development)

### Setup with Docker

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/agent-marketplace.git
   cd agent-marketplace
   ```

2. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Web UI: http://localhost
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the API server:
   ```bash
   python main.py
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run serve
   ```

## API Documentation

The API is documented using OpenAPI (Swagger). When the backend is running, you can access the documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

The API uses API key authentication. For testing purposes, you can use the API key `test_key`, which has admin privileges. In a production environment, you would manage API keys securely.

## Features

### Agent Management

- Register new agents with their capabilities
- Search and discover agents by name, tags, or capabilities
- Execute agents with custom input data
- View execution history and results

### OpenAI Agents Framework Compatibility

The service implements the necessary manifest endpoint and plugin interfaces to be compatible with the OpenAI Agents framework, allowing agents registered in this marketplace to be discovered and used by OpenAI agents.

## Directory Structure

```
agent-marketplace/
├── backend/               # FastAPI application
│   ├── main.py            # Main application entry point
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend Docker configuration
├── frontend/              # Vue.js application
│   ├── src/               # Vue source code
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   ├── Dockerfile         # Frontend Docker configuration
│   └── nginx.conf         # Nginx configuration for production
└── docker-compose.yml     # Docker Compose configuration
```

## License

[MIT License](LICENSE)
