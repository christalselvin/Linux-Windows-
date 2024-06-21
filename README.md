# Flask Web Interface for Executing Windows PowerShell and Linux Bash Commands

This Flask application provides a web interface to execute commands on both Windows and Linux systems. It leverages `pypsrp` for PowerShell commands on Windows and `paramiko` for SSH commands on Linux.

## Features

- User authentication
- Execute PowerShell commands on a Windows machine
- Execute Bash commands on a Linux machine
- Display command results in the web interface

## Requirements

- Python 3.6 or higher
- Flask
- pypsrp
- paramiko

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/christalselvin/Linux-Windows-.git
    cd your-repo-name
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `requirements.txt` file with the following contents:
    ```sh
    Flask
    pypsrp
    paramiko
    ```

## Configuration

1. Update the `main.py` file with your credentials and server details:
    ```python
    common_username = "your_windows_username"
    common_password = "your_windows_password"
    windows_hostname = "localhost"
    windows_port = 5985

    linux_hostname = ""
    linux_port = 22
    linux_username = "root"
    linux_password = ""
    ```

## Usage

1. Run the Flask application:
    ```sh
    python main.py
    ```

2. Open your web browser and go to `http://localhost:5000`.

3. Log in with the following credentials:
    - Username: `1234`
    - Password: `abcd`

4. Use the web interface to execute commands on the Windows or Linux machine.

## Images 
![Screenshot 2024-06-21 235430](https://github.com/christalselvin/Linux-Windows-/assets/127867279/cf62bd29-3aab-4a61-9644-939c64465d34)
![Screenshot 2024-06-21 234820](https://github.com/christalselvin/Linux-Windows-/assets/127867279/f5998d03-86af-4b2f-843e-40d67d483c65)
![Screenshot 2024-06-21 235756](https://github.com/christalselvin/Linux-Windows-/assets/127867279/f95a374f-0a1c-4ff0-996c-8652437aa695)

## File Structure

- `main.py`: Main application file containing the Flask routes and command execution functions.
- `templates/`: Directory containing HTML templates.
  - `login.html`: Login page template.
  - `gridsystem.html`: Main interface after login.
  - `search.html`: Interface for executing PowerShell commands.
  - `linuxsearch.html`: Interface for executing Bash commands.



