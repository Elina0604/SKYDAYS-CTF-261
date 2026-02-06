# 🏴 Order 66: Execute the Query - CTF Challenge

## Challenge Description

**Category:** Web Security / SQL Injection  
**Difficulty:** Intermediate  
**Flag Format:** `SKYDAYS{...}`

The Galactic Empire has deployed a new task management system for coordinating Order 66. Intelligence suggests that critical information is hidden within their database, but the system appears secure at first glance.

Your mission: **Extract the hidden flag from the Imperial database** using any means necessary. The sorting functionality seems particularly interesting...

> *"Execute Order 66. Wipe out the rebellion... and find what they're hiding."*  
> — Darth Vader

## Objective

Extract the flag from the Empire's database by exploiting vulnerabilities in the todo management system.

## Learning Outcomes

By completing this challenge, you will learn:
- **ORDER BY SQL Injection** techniques
- **Boolean-based blind SQL injection** 
- Using **conditional SQL statements** (CASE/IF) for data extraction
- **Automating iterative attacks** with Python/JavaScript
- **Database enumeration** and structure discovery

## Setup Instructions

### Prerequisites
- Python 3.8+ (for backend)
- Bun or Node.js 18+ (for frontend) 
- Basic knowledge of SQL and web exploitation

### Quick Start

1. **Clone the challenge:**
   ```bash
   git clone <repository-url>
   cd order-66
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **Frontend Setup:** (in new terminal)
   ```bash
   cd vader-todo-app
   bun install  # or npm install
   bun dev --port 3000  # or npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - API Info: http://localhost:8000/api/info

## Challenge Hints

### Getting Started
1. **Explore the application** - Create some todos, try different sorting options
2. **Check the API documentation** at `/docs` - What parameters does the todo endpoint accept?
3. **Test the sorting functionality** - What happens when you modify the `sort` parameter?
4. **Look for error messages** - They might reveal interesting information about the database structure

### Technical Hints
1. The vulnerability lies in the **ORDER BY** clause of SQL queries
2. You can use **conditional statements** to extract data character by character
3. The target data is stored in a table that's **not part of the normal todo functionality**
4. **Boolean-based blind injection** will be your primary technique
5. Consider **automating your attack** - manual extraction will be tedious

### Advanced Tips
1. Try payloads like: `(CASE WHEN condition THEN column1 ELSE column2 END)`
2. Look for changes in the **order of returned results** to detect true/false conditions
3. The flag follows the format: `SKYDAYS{...}`
4. Use **SUBSTR()** or **SUBSTRING()** functions for character-by-character extraction

## Expected Solution Approach

1. **Discover the injection point** in the sort parameter
2. **Enumerate database tables** to find where sensitive data is stored  
3. **Extract table structure** to understand column names
4. **Use conditional ORDER BY** to perform boolean-based blind injection
5. **Automate the process** to extract the flag character by character

## Challenge Architecture

### Backend (FastAPI + SQLAlchemy)
- **Vulnerable endpoint:** `GET /api/todos?sort=[PAYLOAD]`
- **Database:** SQLite with `todos` and `flags` tables
- **Vulnerability:** Direct string concatenation in ORDER BY clause

### Frontend (Vue 3)
- **Interface:** Modern todo application with sorting controls
- **Purpose:** Provides a realistic attack surface for testing

## Submission

Submit the flag in the format: `SKYDAYS{...}`

## Flag Verification

You can verify your flag by checking if it matches the pattern and contains Imperial-themed content related to Order 66.

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check Python version (3.8+ required)
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

**Frontend not loading:**
- Ensure backend is running first
- Check if port 3000 is available  
- Try: `bun install && bun dev` or `npm install && npm run dev`

**No todos showing:**
- The application auto-populates with sample Imperial todos
- Try refreshing the page or checking the browser console for errors

### Getting Stuck?

1. **Read the error messages carefully** - they contain valuable information
2. **Test with simple payloads** first before complex injection attempts
3. **Check the API documentation** at `/docs` for parameter details
4. **Look at the network requests** in browser developer tools
5. **Remember:** This is an ORDER BY injection, not a typical WHERE clause injection

## Security Notice

This application contains **intentional vulnerabilities** for educational purposes. 
- **Never deploy this code in production**
- **Only use these techniques in authorized environments**
- **Always practice responsible disclosure**

## Author Credits

Challenge created by transforming the "Vader Todo" application into a SQL injection CTF scenario.

**Original Application:** Vue 3 + FastAPI Todo App with Star Wars theme  
**CTF Adaptation:** SQL Injection vulnerability in sorting functionality

---

*"Your lack of SQL knowledge is disturbing. But fear not, the dark side will teach you..."* - Darth Vader

May the Force (and your SQL skills) be with you! 🌟