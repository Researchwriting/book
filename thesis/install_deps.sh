#!/bin/bash
# Quick Fix for Thesis Generator

echo "🔧 Installing required dependencies..."

# Install pandas and openpyxl via apt
sudo apt update
sudo apt install -y python3-pandas python3-openpyxl python3-requests

# Install python-docx (if not already installed)
sudo apt install -y python3-docx || pip3 install --user python-docx --break-system-packages

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Now run the thesis generator:"
echo "  cd /home/gemtech/Desktop/map"
echo "  python3 test_thesis.py"
echo ""
