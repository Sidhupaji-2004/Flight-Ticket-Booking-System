# Flight Ticket Booking System 🛫💺

A Flight Ticket Booking System built using Django, HTML, CSS, JavaScript, SQLite3, and Python.

<div class="image-container">
    <img src="https://github.com/user-attachments/assets/46681a04-74c8-4acb-8e73-b46779327ef0" alt="Image 1" width="200" height="200">
    <img src="https://github.com/user-attachments/assets/662992fa-2191-492e-a484-b58b3070380e" alt="Image 2" width="200" height="200">
    <img src="https://github.com/user-attachments/assets/dcc41075-aedb-4e0d-a3e9-8ca5d4303b6a" alt="Image 3" width="350" height="200">
    <img src="https://github.com/user-attachments/assets/03b69341-965e-46b4-ba42-a308ed07f5ad" alt="Image 4" width="300" height="150">
    <img src="https://github.com/user-attachments/assets/1f941a16-e5b5-4af7-9265-70854db560f1" alt="Image 5" width="200" height="200">
    <img src="https://github.com/user-attachments/assets/10972a99-dd5b-47a0-bce8-6baeeb4e0839" alt="Image 6" width="200" height="200">
</div>

<style>
    .image-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        align-items: center;
    }
    .image-container img {
        max-width: 100%;
        height: auto;
        margin: 10px;
        flex: 1 1 calc(33.333% - 20px);
        box-sizing: border-box;
    }
</style>


## Description ℹ️

The Flight Ticket Booking System is a web application that allows users to search for flights, view flight details, and book tickets online. It provides a seamless user experience for managing flight bookings, incorporating a range of features for both administrators and users.

![image](https://github.com/user-attachments/assets/b7c1b364-6758-4148-83dd-c6ef62d622ec)


## Features ✨

- **User Authentication**: Secure user registration and login functionality.
- **Flight Search**: Search for available flights based on origin, destination, date, etc.
- **Booking Management**: Book tickets, view booking details, and manage bookings.
- **Admin Panel**: Separate dashboard for administrators to manage flights, users, and bookings.
- **Payment Integration**: Integration with payment gateways for ticket purchase.
- **Email Notifications**: Send confirmation and email notification to users on web check-in using Gmail SMTP and Django email backend.
- **Web Check-in**: Allow users to perform web check-in for their booked flights with a seat map.
- **Database**: SQLite3 (can be upgraded to other databases like PostgreSQL, MySQL)
- **Other Tools**: Git, GitHub, VS Code, etc.

## Technologies Used 🛠️

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3 (can be upgraded to other databases like PostgreSQL, MySQL)

## Screenshots 📸

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <img src="https://github.com/user-attachments/assets/b2e1ce07-b774-4c93-b5dd-8351b9faa54d" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/02b43ab7-738a-47d8-8dfd-a9815f8bcfd0" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/b273bbf7-a538-410c-8ebd-bb71a40b332f" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/3e125445-18a8-4a60-ae49-f6ef18eb56ec" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/dfba9f3a-b5ad-437b-b39a-9dde4aee697d" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/e9e95052-471b-42d0-a251-24157f333209" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/c50c4155-9a45-4143-b50e-8701bce1e9c8" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/718d31b3-e415-44c9-a7f9-b0b192aa0c9c" style="width: 30%; margin: 5px;">
    <img src="https://github.com/user-attachments/assets/8fdd052e-93ae-4762-9959-4c00962b4d42" style="width: 30%; margin: 5px;">
</div>

## Setup Instructions 🚀

Follow these steps to set up and run the Flight Ticket Booking System on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sidhupaji-2004/Flight-Ticket-Booking-System.git
   cd Flight-Ticket-Booking-System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations to set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and go to `http://localhost:8000` to view and interact with the Flight Ticket Booking System.

## Usage 👩‍💻👨‍💻

- **User Registration and Login:** Navigate to `/accounts/register/` to create a new user account or `/accounts/login/` to log in.
- **Flight Search:** Use the search feature to find flights based on origin, destination, and date.
- **Booking Management:** Book tickets for available flights, view booking details, and manage bookings through the user dashboard.
- **Administrator Panel:** Access `/admin/` to manage flights, users, and bookings via a dedicated admin interface.
- **Payment Integration:** Seamless integration with payment gateways for secure online transactions.
- **Email Notifications:** Automatic email notifications and confirmations for booking and web check-in operations.
- **Web Check-in:** Convenient web check-in feature allowing users to select seats using a seat map.

## Contributing 🤝

Contributions and feature requests are welcome! Please fork the repository, make your changes, and submit a pull request.

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
## Explanation:
- **Description**: Provides an overview of the system's purpose and capabilities.
- **Features**: Lists key functionalities of the system.
- **Technologies Used**: Specifies the technologies employed in both backend and frontend development.
- **Screenshots**: Displays screenshots of the application to visually showcase its interface and functionality.
- **Setup Instructions**: Provides detailed steps for cloning, setting up the environment, installing dependencies, applying migrations, and running the development server.
- **Usage**: Describes how users can interact with the application, from registration and login to booking management and admin tasks.
- **Contributing**: Encourages contributions and outlines the process for contributing to the project.
- **License**: Specifies the project's licensing terms for clarity on usage and distribution rights.
