import json
import requests

BASE_URL = "http://localhost:9091"
API_KEY = "test_key"


def register_agent():
    url = f"{BASE_URL}/agents"

    agent_data = {
        "name": "Text Summarizer",
        "description": "An agent that summarizes long pieces of text into concise bullet points",
        "version": "1.0.0",
        "author": "ExampleCorp",
        "contact_email": "support@example.com",
        "homepage_url": "https://example.com/summarizer",
        "api_endpoint": "https://api.example.com/summarize",
        "capabilities": [
            {
                "name": "summarize_text",
                "description": "Summarize a long text into concise bullet points",
                "parameters": {
                    "text": {
                        "type": "string",
                        "description": "The text to summarize"
                    },
                    "max_bullets": {
                        "type": "integer",
                        "description": "Maximum number of bullet points to return",
                        "default": 5
                    },
                    "language": {
                        "type": "string",
                        "description": "Output language",
                        "default": "en"
                    }
                }
            }
        ],
        "auth_type": "api_key",
        "auth_details": {
            "header_name": "X-API-Key"
        },
        "pricing_model": "pay_per_call",
        "pricing_details": {
            "cost_per_call": 0.01,
            "currency": "USD"
        },
        "tags": ["text", "summarization", "nlp"]
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.post(url, headers=headers, json=agent_data)

    if response.status_code == 201:
        print("Agent registered successfully!")
        print(json.dumps(response.json(), indent=2))
        return response.json()["agent_id"]
    else:
        print(f"Failed to register agent: {response.status_code}")
        print(response.text)
        return None


def execute_agent(agent_id):
    url = f"{BASE_URL}/agents/{agent_id}/execute"

    execution_data = {
        "agent_id": agent_id,
        "input_data": {
            "text": """
            Artificial intelligence (AI) is intelligence demonstrated by machines,
            as opposed to intelligence displayed by humans or other animals. Example
            tasks in which this is done include speech recognition, computer vision,
            translation between natural languages, as well as other mappings of inputs.
            AI applications include advanced web search engines, recommendation systems,
            human speech recognition, autonomous driving, automated decision-making
            and competing at the highest level in strategic game systems.
            """
        },
        "execution_parameters": {
            "max_bullets": 3,
            "language": "en"
        },
        "auth_credentials": {
            "api_key": "sample_api_key"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.post(url, headers=headers, json=execution_data)

    if response.status_code == 200:
        print("Agent executed successfully!")
        print(json.dumps(response.json(), indent=2))
        return response.json()["id"]
    else:
        print(f"Failed to execute agent: {response.status_code}")
        print(response.text)
        return None


def list_agents():
    url = f"{BASE_URL}/agents"

    params = {
        "capabilities": ["summarize_text"],
    }

    headers = {
        "X-API-Key": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("Agents found:")
        agents = response.json()["agents"]
        for agent in agents:
            print(f"- {agent['name']} (ID: {agent['id']})")
            print(f"  Description: {agent['description']}")
            print()
    else:
        print(f"Failed to search agents: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    agent_id = register_agent()

    if agent_id:
        execution_id = execute_agent(agent_id)
        list_agents()
