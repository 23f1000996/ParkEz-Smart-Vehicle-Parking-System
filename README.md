# Vehicle Parking App

This is a multi-user web application for managing 4-wheeler parking lots and parking spots, developed using Flask, SQLite, Bootstrap, and Jinja2.

## Features

- User registration and login with role-based access (admin/user)
- Admin dashboard for managing lots and viewing bookings
- Automated parking spot allocation and reservation
- Cost calculation based on parking duration (optional future enhancement)
- Booking logs and history
- Form validation and error handling using Flask-WTF
- Mobile-friendly responsive design using Bootstrap

## Tech Stack

- Flask – Python-based micro web framework
- SQLite – Lightweight file-based database
- Flask-SQLAlchemy – ORM for database management
- Jinja2 – Templating engine for HTML rendering
- Bootstrap 5 – Frontend styling and responsive UI

## Folder Structure

vehicle_parking_app/
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML Templates (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin_panel.html
│   └── ...
├── app.py                # Main Flask app
├── models.py             # Database models (User, ParkingLot, Bookings)
├── forms.py              # Flask-WTForms for validation
├── config.py             # Configuration (database URI, secret key)
└── README.md             # Project documentation (this file)

## Database Schema Overview

### User
| Field     | Type    | Description               |
|---------- |-------- |-------------------------- |
| id        | Integer | Primary key               |
| username  | String  | Unique, required          |
| password  | String  | Hashed, required          |
| role      | String  | 'admin' or 'user'         |

### ParkingLot
| Field        | Type    | Description       |
|------------- |-------- |------------------ |
| id           | Integer | Primary key       |
| lot_number   | String  | Unique identifier |
| is_available | Boolean | True/False        |

### Booking
| Field     | Type       | Description                     |
|---------- |----------- |-------------------------------- |
| id        | Integer    | Primary key                     |
| user_id   | ForeignKey | Linked to User table            |
| lot_id    | ForeignKey | Linked to ParkingLot table      |
| timestamp | DateTime   | Date and time of the booking    |

### Run the app
python app.py
Visit http://localhost:5000 in your browser.
