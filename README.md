# marketplace

**marketplace** provides an agent marketplace for the agent framework.

## Features

## Installation

1. Clone repository:
   ```
   git clone https://github.com/ai-agentx/marketplace.git
   cd marketplace
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

```bash
python marketplace.py
```

The marketplace will be available at http://localhost:9091 by default.

### API Endpoints

#### System

- `GET /health` - Perform health check
- `GET /manifest` - Get the manifest that describes marketplace's compatibility with the agentx Framework

#### Agents

- `POST /agents` - Register a new agent in the marketplace
- `GET /agents` - List and search for agents in the marketplace
- `GET /agents/search` - Search for agents by capabilities, tags, or query
- `GET /agents/{agent_id}` - Get details of a specific agent
- `POST /agents/{agent_id}/execute` - Execute an agent with the provided input
- `GET /agents/{agent_id}/executions` - List executions of a specific agent
- `GET /agents/{agent_id}/executions/{execution_id}` - Get details of a specific execution
- `DELETE /agents/{agent_id}` - Delete an agent from the marketplace
- `PUT /agents/{agent_id}` - Update an existing agent

### Docker Deployment

```
docker-compose up -d
```

## Reference

- [ruff](https://github.com/astral-sh/ruff)
