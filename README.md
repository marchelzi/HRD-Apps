
# HRD Management App

This Django app allows HRD departments to manage employee, branch, and headquarter information, as well as create documents and leave requests.

## Prerequisites

- Python 3.7 or higher
- Django 3.1 or higher
- PostgreSQL 10 or higher

## Installation

Clone the repository:

    git clone https://gitlab.kartel.dev/widyatama-dsa/reg-b2-kls-a/hrdapps.git

Create a virtual environment and activate it:

    python -m venv venv
    source venv/bin/activate

Install the requirements:

    pip install -r requirements.txt

Migrate the database:

    python manage.py migrate

Create a superuser:

    python manage.py createsuperuser

Usage

To run the development server, use the following command:

    python manage.py runserver

You can then access the app at http://localhost:8000/.

I hope this helps! Let me know if you have any questions.

