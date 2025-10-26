# Quick Start Guide

## 🚀 Get Running in 3 Minutes

### Step 1: Setup (90 seconds)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Test Basic Mode (30 seconds)
```bash
python robot_driver.py
```

**Expected Output:**
```
============================================================
Robot Driver - Automated Product Search
============================================================
Navigating to Amazon...
Searching for 'wireless mouse'...

✓ Success! Product: Logitech M510...
✓ Price: $18.99
============================================================
```

### Step 3 (Optional): Test AI Mode

**Setup (.env file needed):**
```bash
# Create .env file with your Anthropic API key
echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key-here" > .env
# Get your key from: https://console.anthropic.com
```

**Run:**
```bash
python ai_robot_driver.py
```

### Step 4 (Optional): Test API Mode

**Start Server:**
```bash
python api.py
```

**Test Endpoint:**
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "mode": "basic"}'
```

**Or visit:** http://localhost:8000/docs

## 📁 Files Overview

| File | Purpose | Required For |
|------|---------|--------------|
| `robot_driver.py` | Basic automation | Required Core ✅ |
| `ai_robot_driver.py` | AI-powered automation | Optional Challenge 1 🤖 |
| `api.py` | Web API service | Optional Challenge 2 🌐 |
| `test_basic.py` | Testing utility | Development 🧪 |

## 🎯 What Each File Does

### robot_driver.py (Required Core)
- Searches for "wireless mouse" on Amazon
- Reports the price
- Handles errors gracefully
- **Run:** `python robot_driver.py`

### ai_robot_driver.py (AI Mode)
- Accepts plain English goals
- Uses Claude AI to plan steps
- Executes dynamically
- **Requires:** ANTHROPIC_API_KEY
- **Run:** `python ai_robot_driver.py`

### api.py (API Mode)
- HTTP REST API for automation
- Supports both basic and AI modes
- Interactive docs at /docs
- **Run:** `python api.py`

## ⚡ Common Commands

```bash
# Test everything works
python test_basic.py

# Run basic automation
python robot_driver.py

# Run AI automation (requires API key)
python ai_robot_driver.py

# Start web API server
python api.py

# View API docs (after starting server)
open http://localhost:8000/docs
```

## 🐛 Quick Troubleshooting

**"playwright: command not found"**
```bash
playwright install chromium
```

**"ANTHROPIC_API_KEY not found"**
```bash
# AI mode only - skip if just testing basic mode
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

**"Module not found"**
```bash
pip install -r requirements.txt
```

## 📚 Full Documentation

See `README.md` for complete documentation.
See `SUBMISSION.md` for evaluation details.

## ✅ Requirements Checklist

- ✅ **Required Core:** `robot_driver.py` - Works standalone
- ✅ **Optional Challenge 1:** `ai_robot_driver.py` - Needs API key
- ✅ **Optional Challenge 2:** `api.py` - REST API

All challenges completed! 🎉
