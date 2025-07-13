# Messenger

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-PyQt6-green.svg)
![Database](https://img.shields.io/badge/Database-SQLite-orange.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time, one-on-one chat application built with Python. It features a client-server architecture, a rich graphical user interface using PyQt6, and persistent data storage with SQLAlchemy and SQLite.

## ✨ Features

-   **User Authentication**: Secure sign-up and sign-in functionality.
-   **Real-Time Messaging**: Instant text communication between connected users.
-   **Contact Management**: Users can add other registered users to their contact list.
-   **Conversation History**: Chat messages are saved and loaded from a local database.
-   **User Profiles**: View your own profile information.
-   **Profile Customization**: Update your username, password, and profile picture in the settings.

## 🏛️ Architecture

The application is built on a classic **client-server model**.

-   **Server (`server.py`)**: A central, multi-threaded socket server that handles client connections, authenticates users upon connection, and routes messages between them. It is responsible for the real-time communication aspect.

-   **Client (`app.py`)**: A desktop application with a well-defined, layered architecture:
    -   **GUI (`src/gui`)**: The presentation layer, built with PyQt6. It includes all windows, dialogs, and user interface components. The `MainWindow` acts as a view controller, managing which screen (Sign In, Sign Up, Chat) is active.
    -   **Services (`src/services`)**: The business logic layer. It coordinates actions between the GUI and the data layer (e.g., `UserService` handles registration logic by calling `AuthService` and `UserRepository`).
    -   **Repositories (`src/repositories`)**: The data access layer. It is responsible for all database interactions, abstracting the database queries from the rest of the application (e.g., `UserRepository`, `MessageRepository`).
    -   **Networking (`socketmanager.py`)**: A dedicated client-side manager for handling the TCP socket connection to the server.
    -   **Models (`src/models`)**: The data structures of the application, defined using SQLAlchemy ORM (e.g., `User`, `Message`, `Contact`).
    -   **Database (`databasemanager.py`)**: A manager to set up the database engine and sessions.
    -   **Design Patterns**: The **Singleton** design pattern is used extensively for services, repositories, and managers to ensure a single, shared instance of these classes throughout the application's lifecycle.

## 🛠️ Tech Stack

-   **Backend & Frontend**: Python 3
-   **GUI Framework**: PyQt6
-   **Database ORM**: SQLAlchemy
-   **Database**: SQLite
-   **Networking**: `socket` and `threading` standard libraries

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

Make sure you have Python 3.10 or newer installed on your system.

### Installation and Setup

1.  **Clone the repository**
    ```sh
    git clone https://github.com/arashm83/messenger
    cd messenger
    ```

2.  **Create a virtual environment (recommended)**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    Create a `requirements.txt` file with the following content:
    ```
    PyQt6
    SQLAlchemy
    ```
    Then, run the installation command:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Initialize the database**
    The application uses an SQLite database. You must create the database and its tables before running the application for the first time. It is recommended to create a file named `create_db.py` in the root directory with the following content and run it:
    ```python
    # create_db.py
    from src.database.databasemanager import DatabaseManager

    print("Initializing database...")
    db = DatabaseManager()
    db.create_tables()
    print("Database and tables created successfully in 'src/database/messenger.db'")
    ```
    Run the script from the root directory:
    ```sh
    python create_db.py
    ```

## 🏃‍♀️ Usage

To use the application, you must first start the server and then run one or more client instances.

1.  **Start the Server**
    Open a terminal and run:
    ```sh
    python messenger/server.py
    ```
    The server will start listening for connections on `0.0.0.0:443`.

2.  **Run the Client Application**
    Open a new terminal and run:
    ```sh
    python messenger/app.py
    ```
    This will launch the GUI application. You can now sign up for a new account or sign in with an existing one. You can run multiple instances of `app.py` to simulate a conversation between different users.

## 📂 Project Structure

The project follows a structured and layered layout:

messenger/
├── app.py                  # Client application entry point
├── server.py               # Server application entry point
└── src/
    ├── database/
    │   └── databasemanager.py # Manages DB connection and sessions
    ├── functions/
    │   └── singleton.py      # Singleton decorator utility
    ├── gui/
    │   ├── main_window.py      # Main window container (QStackedWidget)
    │   ├── sign_in_window.py
    │   ├── sign_up_window.py
    │   ├── chat_window.py      # Main chat interface
    │   ├── settings_window.py
    │   ├── profile_window.py
    │   └── add_contact_dialog.py
    ├── models/
    │   ├── base.py
    │   ├── user.py
    │   ├── message.py
    │   └── contact.py
    ├── repositories/
    │   ├── UserRepository.py
    │   └── messagerepository.py
    └── services/
        ├── AuthService.py      # Handles auth logic (validation, hashing)
        ├── UserService.py      # Main service for user-related actions
        └── socketmanager.py    # Client-side socket management


## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
