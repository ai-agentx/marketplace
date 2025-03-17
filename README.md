# marketplace

**marketplace** provides an agent marketplace for the agent framework.

## Server

### Clone

```base
git clone https://github.com/ai-agentx/marketplace.git
cd server
```

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
python marketplace.py
```

The marketplace will be available at http://localhost:9091 by default.

### API

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

### Docker

```bash
docker-compose up -d
```

## Web

### Clone

```bash
git clone https://github.com/ai-agentx/marketplace.git
cd web
```

### Install

```bash
npm install
```

### Run

```bash
npm run serve
```

### Access

- Web: http://localhost
- API: http://localhost:9091

### Docker

```bash
docker-compose up -d
```

## Reference

- [ruff](https://github.com/astral-sh/ruff)
