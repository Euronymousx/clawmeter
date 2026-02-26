#!/bin/bash
# ClawMeter GitHub Setup Script
# Run these commands on your local machine

# 1. Create the repo on GitHub first:
# Go to https://github.com/new
# Name: clawmeter
# Description: Free OpenClaw cost tracking dashboard
# Public
# UNCHECK "Add a README file"
# Click "Create repository"

# 2. Then run these commands:

# Clone the prepared code
cd ~
mkdir -p clawmeter
cd clawmeter

# Create the files (copy from the code I provided)
# Or download from this session

# Initialize git
git init
git config user.email "sam@clawmeter.io"
git config user.name "Sam"

# Add all files
git add .
git commit -m "Initial ClawMeter build"

# Connect to GitHub (replace with your actual repo URL)
git remote add origin https://github.com/Euronymousx/clawmeter.git

# Push
git push -u origin main

echo "Done! Check https://github.com/Euronymousx/clawmeter"
