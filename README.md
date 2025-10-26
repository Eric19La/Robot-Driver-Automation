# Robot Driver Automation

An intelligent web automation system built with Python and Playwright, featuring both basic scripted tasks and advanced AI-powered dynamic execution using Claude and Model Context Protocol (MCP).

## 🎯 Project Overview

This project demonstrates three levels of web automation capability:

1. **Required Core** - Basic Playwright automation with error handling
2. **Optional Challenge 1** - AI-powered automation with Claude and MCP
3. **Optional Challenge 2** - REST API for remote task execution

## ✨ Features

### Basic Mode
- ✅ Fixed task automation (product search on Amazon)
- ✅ Robust error handling for timeouts and missing elements
- ✅ Clear console output with success/failure messages
- ✅ Reliable execution with proper wait strategies

### AI Mode (Optional Challenge 1)
- 🤖 Dynamic task execution from plain English goals
- 🧠 Claude AI integration for intelligent decision-making
- 🔄 Step-by-step plan generation and execution
- 📊 Page context analysis using accessibility data
- 🎯 Adaptive behavior based on page state

### API Mode (Optional Challenge 2)
- 🌐 RESTful API built with FastAPI
- 📡 Remote task execution via HTTP endpoints
- 📚 Interactive API documentation (Swagger/OpenAPI)
- 🔍 Health check and status endpoints

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Robot-Driver-Automation
```

2. **Create virtual environment**
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

4. **Configure environment (for AI mode)**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## 📖 Usage

### 1. Basic Mode - Fixed Task Automation

Run the basic robot driver to search for a product:

```bash
python robot_driver.py
```

**Output:**
```
============================================================
Robot Driver - Automated Product Search
============================================================
Navigating to Amazon...
Searching for 'wireless mouse'...

✓ Success! Product: Logitech M510 Wireless Computer Mouse...
✓ Price: $18.99

============================================================
RESULT: Success! Product 'Logitech M510...' found
PRICE: $18.99
============================================================
```

### 2. AI Mode - Dynamic Task Execution

Run the AI-powered driver with natural language goals:

```bash
python ai_robot_driver.py
```

The AI will:
1. Analyze the goal
2. Navigate to relevant websites
3. Interact with page elements dynamically
4. Execute multi-step plans autonomously

**Example Goals:**
- "Go to Amazon and find the price of a wireless mouse"
- "Search for the cheapest laptop on BestBuy"
- "Find contact information on example.com"

### 3. API Mode - Web Service

Start the FastAPI server:

```bash
python api.py
```

The API will be available at `http://localhost:8000`

**Interactive Documentation:** `http://localhost:8000/docs`

#### API Endpoints

**POST /execute** - Execute automation task
```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find the price of wireless mouse on Amazon",
    "mode": "basic"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Success! Product found",
  "mode": "basic",
  "price": "$18.99",
  "product": "wireless mouse"
}
```

**AI Mode Example:**
```bash
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Go to Amazon and find laptop prices",
    "mode": "ai",
    "max_steps": 20
  }'
```

**GET /health** - Check service status
```bash
curl http://localhost:8000/health
```

## 🏗️ Project Structure

```
Robot-Driver-Automation/
├── robot_driver.py          # Basic fixed-task automation
├── ai_robot_driver.py       # AI-powered dynamic automation
├── api.py                   # FastAPI web service
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for sensitive configuration:

```bash
# Required for AI Mode (Optional Challenge 1)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Customizing Tasks

#### Basic Mode
Edit `robot_driver.py` and modify the `search_product_price()` function:

```python
# Change the product to search for
result = await search_product_price("laptop")

# Or modify the search logic entirely
```

#### AI Mode
Simply change the goal in `ai_robot_driver.py`:

```python
goal = "Your custom task in plain English"
result = await driver.execute_goal(goal)
```

## 🧪 Testing

### Manual Testing

**Test Basic Mode:**
```bash
python robot_driver.py
# Expected: Should print product name and price
```

**Test AI Mode:**
```bash
python ai_robot_driver.py
# Expected: Should show step-by-step execution with AI reasoning
```

**Test API:**
```bash
# Terminal 1: Start server
python api.py

# Terminal 2: Test endpoint
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "mode": "basic"}'
```

### Error Handling Tests

The system handles:
- ⏱️ Slow page loads (30s timeout)
- 🚫 Missing elements (graceful fallback)
- 🌐 Network errors (retry logic)
- 🔍 Element not found (multiple selectors)

## 📋 Requirements Checklist

### ✅ Required Core (Foundational Skills)
- [x] Python program using Playwright
- [x] Completes fixed, single task (product search)
- [x] Performs browser actions (navigate, click, type)
- [x] Proper error handling (no crashes)
- [x] Clear console output

### ✅ Optional Challenge 1 (AI + MCP - Advanced Skills)
- [x] AI Language Model integration (Claude)
- [x] Dynamic execution from plain English goals
- [x] Model Context Protocol integration
- [x] Structured page context for AI decision-making
- [x] Step-by-step plan generation

### ✅ Optional Challenge 2 (Deployment Skills)
- [x] Network-accessible API (FastAPI)
- [x] Web access endpoint with message parameter
- [x] Clear setup instructions
- [x] requirements.txt with all dependencies

## 🎓 Skills Demonstrated

### Core Python & Automation
- Async/await programming with asyncio
- Playwright browser automation
- Exception handling and error recovery
- Clean code structure and documentation

### AI & MCP Architecture
- Claude API integration
- Dynamic task planning with LLM
- Structured communication (JSON parsing)
- Context-aware decision making
- Accessibility-based element selection

### Web Services & Deployment
- RESTful API design with FastAPI
- Pydantic models for validation
- OpenAPI/Swagger documentation
- Error handling and HTTP status codes
- Environment-based configuration

### Software Engineering
- Git version control
- Virtual environment management
- Dependency management (requirements.txt)
- Clean documentation (README)
- Code organization and modularity

## 🐛 Troubleshooting

### Common Issues

**Issue: "playwright: command not found"**
```bash
# Make sure to install Playwright browsers
playwright install chromium
```

**Issue: "ANTHROPIC_API_KEY not found"**
```bash
# Create .env file and add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

**Issue: "Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Browser times out**
- Check internet connection
- Increase timeout in code (default: 30s)
- Try with `headless=False` to see what's happening

## 📝 License

This project is created as a sample submission for internship evaluation.

## 👤 Author

Created as part of a software engineering internship application demonstrating skills in:
- Python software engineering
- Web automation (Playwright)
- AI agent architecture (Claude + MCP)
- API design and deployment (FastAPI)
- Software reliability and error handling

## 🔗 Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Note:** This is a demonstration project. The AI mode requires an Anthropic API key (paid service). The basic and API modes work without any external dependencies beyond the Python packages listed.
