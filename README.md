# ParkEz: Smart Vehicle Parking System

Your seamless solution for effortless parking!  
**ParkEz** is a multi-user web application built with **Flask**, enabling administrators and users to efficiently manage parking lots and vehicle bookings.

---

## ✨ Key Features

- **Intuitive Dashboards**: Separate, user-friendly interfaces for Admins and Users.
- **Dynamic Lot Management**: Admins can create, update, and delete parking lots with custom pricing and capacity.
- **Automated Spot Allocation**: Users are assigned the first available spot in their selected lot.
- **Real-Time Occupancy Tracking**: Admins view parking lot status via interactive charts.
- **Cost Calculation**: Users are billed based on parking duration and hourly rate.
- **Secure Authentication**: Separate flows for user and admin login/registration.
- **Responsive UI**: Built with Bootstrap 5 for mobile-friendly usage.

---

## 💻 Tech Stack

| Layer     | Technologies                          |
|-----------|----------------------------------------|
| Backend   | Python, Flask, Flask-SQLAlchemy        |
| Frontend  | HTML5, CSS3, Jinja2, Bootstrap 5       |
| Charts    | Chart.js                               |
| Database  | SQLite                                 |

---

## 🚀 Get Started in Minutes

📁 Repository Structure
csharp
Copy
Edit
parkez/
├── instance/
│   └── parking.db            # SQLite database (auto-generated)
├── static/
│   └── css/
│       └── style.css         # Custom styles
├── templates/
│   ├── admin_dashboard.html  # Admin panel
│   ├── base.html             # Shared layout
│   ├── login.html            # Login form
│   ├── lots.html             # Parking lot booking interface
│   ├── register.html         # Registration page
│   └── user_dashboard.html   # User dashboard
├── app.py                    # Flask app logic
└── README.md                 # Project documentation

### 1️⃣ Clone the Repository

```bash
git clone [https://github.com/your-username/parkez.git
cd parkez](https://github.com/23f1000996/ParkEz-Smart-Vehicle-Parking-System)
