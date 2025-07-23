# 🚗 ParkEz: Smart Vehicle Parking System

> **Your seamless solution for effortless parking management!**
> **ParkEz** is a multi-user web application built with **Flask**, enabling **Admins** and **Users** to efficiently manage parking lots and vehicle bookings.

---

## ✨ Features

* 🔑 **Secure Authentication** for Admins and Users
* 🧭 **Dynamic Parking Lot Management** with custom capacity and pricing
* 🎯 **Auto Spot Allocation** based on real-time availability
* 📊 **Live Dashboard** with charts showing lot status and occupancy
* 🧾 **Cost Calculator** based on duration × hourly rate
* 📱 **Responsive UI** using Bootstrap 5 for a smooth mobile experience

---

## 💻 Tech Stack

| Layer    | Technologies                     |
| -------- | -------------------------------- |
| Backend  | Python, Flask, Flask-SQLAlchemy  |
| Frontend | HTML5, CSS3, Jinja2, Bootstrap 5 |
| Charts   | Chart.js                         |
| Database | SQLite                           |

---

## 🗂️ Project Structure

```bash
parkez/
├── instance/
│   └── parking.db            # SQLite database (auto-generated)
├── static/
│   └── css/
│       └── style.css         # Custom CSS
├── templates/
│   ├── admin_dashboard.html  # Admin Dashboard
│   ├── base.html             # Base template
│   ├── login.html            # Login form
│   ├── lots.html             # Booking interface
│   ├── register.html         # Registration form
│   └── user_dashboard.html   # User Dashboard
├── app.py                    # Flask app logic
└── README.md                 # Project documentation
```

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/23f1000996/ParkEz-Smart-Vehicle-Parking-System.git
cd ParkEz-Smart-Vehicle-Parking-System
```

### 2️⃣ Install Dependencies

Make sure Python is installed. Then:

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask App

```bash
python app.py
```

Now visit `http://127.0.0.1:5000/` in your browser!

---

## 🧪 User Roles

### 👨‍💼 Admin

* Register/Login
* Add/Edit/Delete Parking Lots
* Monitor occupancy and stats in real-time

### 👤 User

* Register/Login
* Book available spots in selected lots
* View booking history and cost

---

## 📈 Visuals

> Admin Dashboard with live pie chart for occupancy
> User Dashboard with active booking summary

*(Screenshots can be added here in the future using `![image](link)`)*

---

## 🛠️ Contributions

Want to improve ParkEz?
Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT License © [Md Irshad Anwar](https://github.com/23f1000996)

---

Let me know if you want to:

* Add demo screenshots or GIFs
* Include Streamlit version in this project too
* Add badges like `Built With Flask`, `MIT License`, etc.
