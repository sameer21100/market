
# Credify Bazaar

Credify Bazaar – A Flask-based mini-market with budget tracking and Razorpay-powered wallet top-ups.

## Live

https://market-zkot.onrender.com


## Authors

- [@sameer21100](https://www.github.com/sameer21100)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

RazorPay Key: `RAZORPAY_KEY_ID`

RazorPay Secret:`RAZORPAY_KEY_SECRET`

PostgreSQL External Link: `DATABASE_URL`


## Features

- User Management
- Marketplace Functionality
- Payments & Budget
- Buyer-Seller Communication


## Tech Stack

	•	Python 3.9
	•	Flask
	•	Gunicorn
	•	SQLite
	•	PostgreSQL
	•	Render
	•	Docker
	•	Razorpay API
	•	SQLAlchemy
	•	Git
	•	GitHub

## Run Locally

Clone the project

```bash
  git clone https://github.com/sameer21100/market
```

Go to the project directory

```bash
  cd market
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  gunicorn app:app
```

