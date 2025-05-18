# Unicorn Companies Analysis Website

This project is a web application for analyzing unicorn companies, built with Django backend and HTML/CSS frontend.

## Features

- List and search unicorn companies
- Data visualization with charts
- Export functionality for analysis data in CSV, Excel, and PDF formats
- Admin interface for managing data
- Improved UI with Bootstrap cards and enhanced layout for better user experience

## Tech Stack

- Backend: Django, Django REST Framework
- Frontend: HTML, CSS, Bootstrap, Chart.js
- Database: SQLite (development), PostgreSQL (production)

## Setup Instructions

1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Usage

- Access the home page to view unicorn companies
- Use the Analysis page to filter data, view charts, and export analysis data
- Export options available for CSV, Excel, and PDF formats with applied filters
- Detailed unicorns data available with improved UI and navigation

## Notes

- Ensure dependencies like pandas and reportlab are installed for export functionality
- UI improvements include Bootstrap cards, responsive layout, and styled export buttons
