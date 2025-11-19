#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting VPS Setup for Textbook Generator...${NC}"

# 1. Update System
echo -e "${GREEN}📦 Updating system packages...${NC}"
dnf update -y

# 2. Install Dependencies (AlmaLinux/RHEL)
echo -e "${GREEN}🛠️ Installing Python, Git, and Tmux...${NC}"
dnf install -y python3 python3-pip git tmux nano

# 3. Set up Virtual Environment
echo -e "${GREEN}🐍 Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# 4. Install Python Requirements
echo -e "${GREEN}📚 Installing Python libraries...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create Output Directory
mkdir -p output

echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "To start the app, run:"
echo -e "  ${GREEN}source venv/bin/activate${NC}"
echo -e "  ${GREEN}python3 -m src.interactive_main${NC}"
