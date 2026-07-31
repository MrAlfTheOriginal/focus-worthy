#!/bin/bash
# Focus Worthy MVP Setup & Quick Start

set -e

echo "==========================================="
echo "Focus Worthy MVP - Setup & Launch"
echo "==========================================="

cd /home/alf/focus-worthy

# Step 1: Install dependencies
echo "Step 1: Installing dependencies..."
pip install -q -r requirements.txt

# Step 2: Initialize databases
echo "Step 2: Initializing databases..."
python3 db.py

# Step 3: Display structure
echo ""
echo "✓ Setup complete!"
echo ""
echo "Project structure:"
ls -lh

echo ""
echo "==========================================="
echo "NEXT STEPS:"
echo "==========================================="
echo ""
echo "Start the backend API:"
echo "  python3 api.py"
echo ""
echo "In another terminal, start the website receiver:"
echo "  python3 website_receiver.py"
echo ""
echo "In a third terminal, start the desktop UI:"
echo "  python3 ui.py"
echo ""
echo "API endpoints:"
echo "  - Affiliate Program Management: http://localhost:5000"
echo "  - Website Product Receiver: http://localhost:5001"
echo ""
echo "Database files:"
echo "  - Affiliate platform: focus_worthy.db"
echo "  - Website: website.db"
echo ""
echo "==========================================="
