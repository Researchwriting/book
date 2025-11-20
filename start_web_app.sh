#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting AI Textbook Web App...${NC}"

# Activate venv
source venv/bin/activate

# Install dependencies if missing (fast check)
if ! python3 -c "import fastapi" &> /dev/null; then
    echo -e "${BLUE}📦 Installing web dependencies...${NC}"
    pip install fastapi uvicorn python-multipart
fi

# Get local IP
IP=$(hostname -I | awk '{print $1}')

echo -e "${GREEN}✅ Web App Running!${NC}"
echo -e "📱 Access it here: ${BLUE}http://$IP:8000/static/index.html${NC}"
echo -e "💻 Local access:   ${BLUE}http://localhost:8000/static/index.html${NC}"
echo -e "(Press Ctrl+C to stop)"

# Run API
python3 -m uvicorn src.api:app --host 0.0.0.0 --port 8000
