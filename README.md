# 🏨 Hotel Management System

A Python + MySQL based Hotel Management System that manages hotel operations through a command-line interface.

This project allows an admin to manage customers, rooms, bookings, billing, and other hotel activities efficiently using a database-driven system.

## 🚀 Features

- Admin Login System
- Customer Check-In
- Customer Check-Out
- Automatic Bill Generation
- Room Management
- Add New Rooms
- Modify Room Prices
- Update Room Status
- View Customer Details
- View Booking History
- Change Admin Password
- MySQL Database Integration

## 🛠️ Technologies Used

- Python
- MySQL
- mysql-connector-python
- python-dotenv

## 📂 Project Structure

Hotel-Management-System/

├── HotelManagementSystem.py  
├── README.md  
├── requirements.txt  
├── .gitignore  
└── .env.example  


## ⚙️ Installation and Setup

Follow these steps to run this project on your local machine.

### 1. Clone the repository

Open your terminal and run:

git clone https://github.com/Somay-Yadav/Hotel-Management-System.git


### 2. Open the project folder

Navigate into the project directory:

cd Hotel-Management-System


### 3. Install required dependencies

Install all required Python libraries:

pip install -r requirements.txt


### 4. Setup MySQL Database

Make sure MySQL is installed and running on your system.

Rename `.env.example` file to `.env` file in the project folder and add your MySQL details:

MYSQL_HOST=localhost

MYSQL_USER=root

MYSQL_PASSWORD=your_password


Replace `your_password` with your actual MySQL password.

### 5. Run the application

Start the hotel management system using:

python HotelManagementSystem.py


## 🔐 Default Login

Username:

admin

Password:

1234

You can change the password after logging into the system.

## 📚 Learning Goals

This project helped me practice:

- Python programming
- MySQL database connectivity
- SQL queries
- CRUD operations
- Database management
- Environment variable handling
- Building real-world projects

## 🔮 Future Improvements

Some improvements planned for future versions:

- Add a graphical user interface (GUI) using Tkinter or PyQt
- Add employee/staff management system
- Add online room booking feature
- Add customer registration and profile management
- Generate downloadable PDF bills
- Add advanced search and filtering options
- Improve security with encrypted passwords
- Add user roles and permissions (Admin/Staff)
- Add email confirmation for bookings
- Create a web-based version using Flask/Django
- Improve database design and optimization
- Add dashboard with hotel statistics and reports

## 👨‍💻 Author

Somay Yadav

GitHub:
https://github.com/Somay-Yadav

---

⭐ If you like this project, consider giving it a star!