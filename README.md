# E-commerce Multi-Agent System

A powerful e-commerce platform built with CrewAI that uses multiple AI agents to provide intelligent product search, price comparison, personalized recommendations, and customer support.

## 🚀 Features

- **Multi-Agent Architecture**: Four specialized AI agents working together
  - **Product Research Specialist**: Searches and analyzes products based on customer requirements
  - **Price Analyzer**: Compares prices across platforms and finds the best deals
  - **Recommendation Specialist**: Creates personalized product recommendations
  - **Customer Service Agent**: Provides excellent customer support and assistance

- **REST API**: FastAPI-based web service with comprehensive endpoints
- **Redis Caching**: Intelligent caching for improved performance
- **Real-time Processing**: Asynchronous task handling for complex searches
- **Interactive CLI**: Command-line interface for direct interaction

## 🏗️ Architecture

```
E-commerce Multi-Agent System
├── FastAPI Web Service (Port 8000)
├── CrewAI Multi-Agent Framework
│   ├── Product Research Agent
│   ├── Price Analysis Agent
│   ├── Recommendation Agent
│   └── Customer Service Agent
├── Redis Cache (Optional)
└── Custom E-commerce Tools
```

## 📋 Prerequisites

- Python 3.10 or higher
- Redis (optional, for caching)
- OpenAI API key (or other LLM provider)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd E-commerce-Multi-Agent
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
# or
pip install -e .
```

3. **Set up environment variables**:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export REDIS_HOST="localhost"  # Optional
export REDIS_PORT="6379"       # Optional
```

4. **Start Redis (Optional)**:
```bash
redis-server
```

## 🚦 Quick Start

### 1. Start the API Server

```bash
# Using the script
python -m src.e_commerce.api

# Or using uvicorn directly
uvicorn src.e_commerce.api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 2. Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation

### 3. Using the CLI

```bash
# Run default demo
python -m src.e_commerce.main

# Interactive product search
python -m src.e_commerce.main search

# Customer support mode
python -m src.e_commerce.main support
```

## 📚 API Usage

### Product Search

**POST** `/api/v1/search`

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "wireless bluetooth headphones",
       "budget": "under $200",
       "category": "electronics",
       "preferences": "noise cancellation, long battery life"
     }'
```

**Response**:
```json
{
  "success": true,
  "message": "Product search completed successfully",
  "data": {
    "success": true,
    "result": "...detailed recommendations...",
    "recommendations": "...personalized suggestions..."
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Customer Support

**POST** `/api/v1/support`

```bash
curl -X POST "http://localhost:8000/api/v1/support" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is your return policy?",
       "context": "I am considering buying headphones"
     }'
```

### Get Examples

```bash
# Get search examples
curl "http://localhost:8000/api/v1/search/example"

# Get support examples
curl "http://localhost:8000/api/v1/support/example"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `REDIS_HOST` | Redis server host | localhost |
| `REDIS_PORT` | Redis server port | 6379 |
| `REDIS_DB` | Redis database number | 0 |
| `REDIS_PASSWORD` | Redis password | None |

### Agent Configuration

Agents are configured in `src/e_commerce/config/agents.yaml`:

```yaml
product_researcher:
  role: E-commerce Product Research Specialist
  goal: Research and analyze products based on customer requirements
  backstory: You're an expert e-commerce researcher...
```

### Task Configuration

Tasks are defined in `src/e_commerce/config/tasks.yaml`:

```yaml
product_search_task:
  description: Search for products based on customer requirements
  expected_output: A detailed list of product recommendations
  agent: product_researcher
```

## 🛠️ Development

### Project Structure

```
src/e_commerce/
├── __init__.py
├── main.py              # CLI interface
├── api.py              # FastAPI web service
├── crew.py             # CrewAI implementation
├── config/
│   ├── agents.yaml     # Agent configurations
│   └── tasks.yaml      # Task definitions
└── tools/
    ├── __init__.py
    ├── custom_tool.py   # Template for custom tools
    └── ecommerce_tools.py # E-commerce specific tools
```

### Adding New Agents

1. Define the agent in `config/agents.yaml`
2. Add corresponding tasks in `config/tasks.yaml`
3. Implement the agent in `crew.py`

### Adding New Tools

Create tools in `src/e_commerce/tools/`:

```python
from crewai.tools import BaseTool
from pydantic import BaseModel

class MyToolInput(BaseModel):
    query: str

class MyTool(BaseTool):
    name: str = "My Custom Tool"
    description: str = "Description of what this tool does"
    args_schema: Type[BaseModel] = MyToolInput
    
    def _run(self, query: str) -> str:
        # Tool implementation
        return "Tool result"
```

## 🧪 Testing

### Run Tests

```bash
# Test the crew
python -m src.e_commerce.main test

# Train the crew
python -m src.e_commerce.main train 5 training_results.json
```

### API Testing with curl

```bash
# Health check
curl "http://localhost:8000/health"

# Search for products
curl -X POST "http://localhost:8000/api/v1/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "smartphone", "budget": "under $500"}'
```

## 🔍 Monitoring

### Redis Cache Statistics

The system provides cache statistics when Redis is connected:

```python
from reddis import get_redis_client

client = get_redis_client()
stats = client.get_cache_stats()
print(stats)
```

### Logs

The application uses structured logging. Key log events include:
- Agent execution start/completion
- Cache hits/misses
- API request processing
- Error handling

## 🚀 Deployment

### Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.e_commerce.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **Database**: Consider using a persistent database for user data
3. **Load Balancing**: Use nginx or similar for production loads
4. **Monitoring**: Implement proper monitoring and alerting
5. **Security**: Add authentication and rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

1. Check the [documentation](http://localhost:8000/docs)
2. Create an issue on GitHub
3. Contact the development team

## 🎯 Roadmap

- [ ] Integration with real e-commerce APIs (Amazon, eBay, etc.)
- [ ] Advanced user profiling and ML-based recommendations
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Order management system
- [ ] Payment integration

---

**Happy Shopping with AI! 🛒🤖**

# 🛒 Autonomous E-Commerce Manager
## 🔍 Problem It Solves: 
    Online sellers need to manage pricing, inventory, marketing, and customer queries manually. 
    Automation here means scale and reduced operational overhead.
## 🧠 Agentic System Overview: 
    - 📦 Inventory Manager Agent: Monitors stock levels and auto-restocks or alerts. 
    - 💸 Pricing Agent: Adjusts prices based on demand, competitor pricing, or click-throughs. 
    - 📢 Marketing Agent: Writes product descriptions, creates social posts, and schedules ads. 
    - 💬 Customer Support Agent: Responds to inquiries. 
    - 📊 Sales Analyst Agent: Analyzes trends and suggests actions (e.g., bundling products).
## 💡 Tech Stack: 
    - LLMs: ollama, DeepSeek-r1:8b 
    - Laguage: Python
    - Data: MongoDB, Redis 
    - Agent Frameworks: CrewAI
## 🚀 Example Use: 
      “You are selling eco-friendly bottles. Sales are dropping.” → Sales Analyst Agent finds dip from mobile users 
      → Pricing Agent runs a 10% mobile discount → Marketing Agent sends Instagram promo → Inventory Agent checks stock levels
