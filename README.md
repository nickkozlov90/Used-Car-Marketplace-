# used-car-marketplace
Welcome to the Used Car Marketplace! This is a Django-based web application that allows users to buy and sell used cars online.

## Project Overview
The Used Car Marketplace is a platform where users can:

 - Browse and search for used cars listed by sellers.
 - Create user accounts and profiles.
 - List their used cars for sale, including details such as price, model, mileage and photo.
 - Create personal list of favourite listings.
 - Contact sellers and negotiate deals.
 - Administer and manage their listings through a user-friendly dashboard.

## Prerequisites
Before you begin, ensure you have met the following requirements:

 - Python 3.10.10
 - Django 4.2.5
 - List of other requirements you can find in 'requirements.txt' file.

## Installation
Follow these steps to set up the project locally:

1. Clone the repository and switch to the project directory:

    ```bash
    git clone https://github.com/nickkozlov90/used-car-marketplace.git
    cd used-car-marketplace
    ```

2. Create a virtual environment:

    ```bash
   python -m venv venv
    ```

3. Activate the virtual environment:

   On Windows: 
   ```bash
    venv\Scripts\activate
    ```
   On macOS and Linux:
   ```bash
   source venv/bin/activate
   ```
   
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. Copy this file ".env_sample" and rename it to ".env", then fill in the actual values for your local development environment.

## Usage

1. Apply the migrations:

   ```bash
   $ python manage.py migrate
      ```

2. To run the development server, use the following command:

   ```bash
   python manage.py runserver
   ```

Access the application in your web browser at http://localhost:8000.





## Project Fixture Files

 - This project includes fixture files that are used for testing and demonstration purposes.
The fixture files contain sample data representing various user profiles, car models and listings.
 - You can find the fixture file is named `marketplace_db_data.json` in the root directory.
 - To load the fixture data into the application, use the following command:

   ```bash
   python manage.py loaddata marketplace_db_data.json
   ```
