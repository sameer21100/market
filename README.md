
# Sam's Bazaar

A Flask-based mini-market with budget tracking and Razorpay-powered wallet top-ups.

## Live

https://online-bazzar.onrender.com


## Authors

- [@sameer21100](https://www.github.com/sameer21100)

## Screenshots
<img width="1470" height="956" alt="Screenshot 2025-08-19 at 12 51 33 PM" src="https://github.com/user-attachments/assets/bf8dcdb3-de73-4e95-9f04-e506ccd9f343" />
<img width="1470" height="956" alt="Screenshot 2025-08-19 at 12 51 26 PM" src="https://github.com/user-attachments/assets/37ec7d73-3a59-4358-b62c-d28b90a5690d" />
<img width="1470" height="956" alt="Screenshot 2025-08-19 at 12 51 48 PM" src="https://github.com/user-attachments/assets/d15905db-9a38-4cb9-b072-f740c4bccb3a" />
<img width="1470" height="956" alt="Screenshot 2025-08-19 at 12 58 53 PM" src="https://github.com/user-attachments/assets/8ffa3181-6607-46c2-8ee5-c4d91465d085" />


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

