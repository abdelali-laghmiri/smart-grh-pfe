# 🚀 Smart GRH – Intelligent Human Resource Management System

## 📌 Project Overview

**Smart GRH** is an intelligent Human Resource Management (HRM) system developed as a Final Year Project (PFE).

The system aims to automate and optimize HR processes within small and medium-sized enterprises (SMEs).

It focuses on:

- Structured request management  
- Multi-level approval workflows  
- NFC-based attendance tracking  
- Monthly performance evaluation  
- Real-time HR dashboard with KPIs  

---

## 🎯 Project Objectives

- Centralize employee management in a unified system  
- Implement dynamic multi-level approval workflows  
- Automate leave validation and monthly leave accrual  
- Track attendance using NFC-based IN/OUT scanning  
- Generate automatic monthly performance scores  
- Provide decision-support dashboards for HR  

---

## 🏗️ System Architecture

The application follows a 3-tier architecture:

- **Frontend:** Django Templates (MVC pattern)  
- **Backend:** Django (Business Logic + API)  
- **Database:** MySQL  

Frontend  →  Django Backend  →  MySQL Database  

---

## 🧠 Core Modules

### 1️⃣ Organizational Structure

- Departments  
- Teams  
- Job Positions (with hierarchy levels)  
- Self-referencing manager hierarchy  

Each employee has a job position, belongs to a team and department, and may have a direct manager.

---

### 2️⃣ Request Management Engine

- Configurable request types  
- One workflow per request type  
- Multi-level approval  
- Hierarchical approval (manager chain)  
- Role-based approval (HR department)  
- Mixed approval models  
- Approval history tracking  
- Employee cancellation before final approval  

---

### 3️⃣ Attendance Management

- NFC-based IN / OUT scanning  
- Automatic delay calculation  
- One attendance record per day  
- Late detection and reporting  

---

### 4️⃣ Performance Module

- Monthly performance calculation  
- Attendance-based automatic scoring  
- Optional HR evaluation  
- Final performance score generation  

Performance is computed using attendance indicators and optionally adjusted by HR evaluation.

---

### 5️⃣ Automation Engine

The system integrates multiple automation rules:

- Automatic leave balance validation before approval  
- Monthly leave accrual based on job position  
- Dynamic approver detection  
- Automatic notifications  
- KPI aggregation for dashboards  

---

## 🔄 Approval Workflow Logic

Each **Request Type** is associated with:

- One Approval Workflow  
- Multiple ordered Approval Steps  

Each step defines:

- Required Job Position  
- Whether to use hierarchy  
- Optional department restriction  

This design allows:

- Pure hierarchical approval  
- Pure role-based approval  
- Mixed approval models  

---

## 🗂️ Main Database Entities

- User (Django built-in authentication)  
- UserProfile  
- Department  
- Team  
- JobPosition  
- Request  
- RequestType  
- ApprovalWorkflow  
- ApprovalStep  
- ApprovalHistory  
- Attendance  
- Performance  
- Notification  
- LeaveAdjustment  

---

## 📊 UML Diagrams

### 🔹 Class Diagram

![Class Diagram](uml/use_cases/CD%20-%20Smart%20GRH%20(Final%20Version).png)

### 🔹 Use Case Diagram

![Use Case Diagram](uml/use_cases/UC%20-%20Smart%20GRH%20(Global).png)

### 🔹 Sequence Diagram

![Sequence Diagram](uml/use_cases/SD%20-%20Request%20Workflow%20(Functional).png)



---

## ⚙️ Technologies Used

- Python 3  
- Django  
- MySQL  
- HTML / CSS / Bootstrap  
- Git & GitHub  

---

## 🛠️ Installation Guide

1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies  
4. Run migrations  
5. Start the server  

### Commands

git clone https://github.com/abdelali-laghmiri/smart-grh-pfe.git  
cd smart-grh-pfe  
python -m venv venv  
venv\Scripts\activate   # Windows  
pip install -r requirements.txt  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

---

## 🔐 Authentication & Roles

The system uses Django Authentication with Groups:

- Employee  
- HR  
- Admin  

Permissions are managed using Django’s built-in authorization system.

---

## 📈 Dashboard KPIs

HR Dashboard includes:

- Pending Requests  
- Monthly Approvals  
- Late Rate  
- Absence Rate  
- Average Performance Score  

Managers see KPIs related to their teams.  
Employees see personal statistics.

---

## 🚀 Future Improvements

- Email notifications  
- Payroll integration  
- Advanced reporting  
- AI-based performance prediction  

---

## 👨‍🎓 Academic Context

This project was developed as a Final Year Project (PFE), focusing on system modeling, automation logic, and scalable architecture design.

---

## 📄 License

Academic project – for educational purposes only.