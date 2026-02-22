# 👤 Users Module API Documentation

Base URL:
http://127.0.0.1:8000/api/users/

---

# 📁 Departments

## 🔹 GET All Departments
GET /departments/

Response:
[
  {
    "id": 1,
    "name": "HR"
  }
]

---

## 🔹 POST Create Department
POST /departments/

Body:
{
  "name": "HR"
}

Response:
{
  "id": 1,
  "name": "HR"
}

---

## 🔹 GET Department By ID
GET /departments/{id}/

---

## 🔹 PUT Update Department
PUT /departments/{id}/

Body:
{
  "name": "Human Resources"
}

---

## 🔹 DELETE Department
DELETE /departments/{id}/

---

# 📁 Job Positions

## 🔹 GET All Positions
GET /positions/

---

## 🔹 POST Create Position
POST /positions/

Body:
{
  "title": "Manager",
  "level": 3,
  "monthly_leave_accrual": 2
}

Response:
{
  "id": 1,
  "title": "Manager",
  "level": 3,
  "monthly_leave_accrual": 2
}

---

## 🔹 GET Position By ID
GET /positions/{id}/

---

## 🔹 PUT Update Position
PUT /positions/{id}/

Body:
{
  "title": "Senior Manager",
  "level": 4,
  "monthly_leave_accrual": 2.5
}

---

## 🔹 DELETE Position
DELETE /positions/{id}/

---

# 📁 Teams

## 🔹 GET All Teams
GET /teams/

---

## 🔹 POST Create Team
POST /teams/

Body:
{
  "name": "Team A",
  "departement": 1
}

Response:
{
  "id": 1,
  "name": "Team A",
  "departement": 1
}

---

## 🔹 GET Team By ID
GET /teams/{id}/

---

## 🔹 PUT Update Team
PUT /teams/{id}/

Body:
{
  "name": "Team Alpha",
  "departement": 1
}

---

## 🔹 DELETE Team
DELETE /teams/{id}/

---

# 📁 User Profiles

## 🔹 GET All Profiles
GET /profiles/

Response:
[
  {
    "id": 1,
    "user": {
      "username": "ali",
      "email": "ali@test.com"
    },
    "leave_balance": 5.0,
    "job_position": 1,
    "departement": 1,
    "team": 1,
    "manager": null
  }
]

---

## 🔹 POST Create Profile
POST /profiles/

Body:
{
  "user": {
    "username": "ali",
    "email": "ali@test.com"
  },
  "job_position": 1,
  "departement": 1,
  "team": 1,
  "manager": null,
  "leave_balance": 5
}

Notes:
- username must be unique
- departement, job_position, team must exist

---

## 🔹 GET Profile By ID
GET /profiles/{id}/

---

## 🔹 PUT Update Profile
PUT /profiles/{id}/

Body:
{
  "job_position": 2,
  "departement": 2,
  "team": 1,
  "manager": null,
  "leave_balance": 10
}

---

## 🔹 DELETE Profile
DELETE /profiles/{id}/

Note:
Deleting profile deletes the associated auth user.