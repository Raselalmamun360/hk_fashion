#!/bin/bash

# Change to the project directory
cd "$(dirname "$0")"

# Set colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running tests for HK Fashion E-commerce Project${NC}"
echo "========================================================"

# Run tests for each app
echo -e "\n${YELLOW}Testing Products App${NC}"
echo "------------------------"
python manage.py test products

echo -e "\n${YELLOW}Testing Cart App${NC}"
echo "------------------------"
python manage.py test cart

echo -e "\n${YELLOW}Testing Orders App${NC}"
echo "------------------------"
python manage.py test orders

echo -e "\n${YELLOW}Testing Users App${NC}"
echo "------------------------"
python manage.py test users

# Run all tests together
echo -e "\n${YELLOW}Running All Tests${NC}"
echo "------------------------"
python manage.py test

echo -e "\n${GREEN}All tests completed!${NC}"