# Vehicle Parking App - V2

A simple multi-user web application that manages parking lots, parking spots, and vehicle reservations for 4‑wheelers. The system has two roles: **Admin** and **User**.

## What the App Does

* The **Admin** can create, edit, and delete parking lots.
* Whenever a parking lot is created, the required number of parking spots are automatically generated.
* The **User** can register and log in.
* Users can book a parking spot from any available parking lot.
* The app automatically assigns the **first available** spot.
* Users can release the spot when they leave.
* The Admin can see all lots, spot statuses, and user information.
* The app sends daily reminder messages through a scheduled background job.

## Frameworks & Technologies Used

* **Flask** – Backend API
* **VueJS** – Frontend UI
* **Bootstrap** – Styling (mandatory CSS framework)
* **SQLite** – Database
* **Redis** – Caching and Celery backend
* **Celery** – Background jobs / scheduled tasks
* **Jinja2** – Only for entry template when using CDN for Vue

## Summary

The app provides a complete parking management system with automatic spot allocation, user registration, admin controls, and background reminders. All functionalities run entirely on the local machine using the required frameworks.
