# Heatstroke-Project
## Getting Started
You have to install software before using the project.
Download [Python](https://www.python.org/downloads/)


### Installation
1. Clone the repo
    ```sh
    git clone https://github.com/6310611030/Heatstroke-Project
    ```
2. Change directory to the project
    ```sh
    cd Heatstroke/heatstroke_warning_system
    ```
3. Set Up a Virtual Environment (Optional but Recommended)
    ```sh
    python -m venv .venv
    ```
4. Activate the virtual environment
   ```sh
    .venv\Scripts\activate
    ```
5. Install requirements for the project
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1. Create a Superuser
    ```sh
    python manage.py createsuperuser
    ```

2. Run Django server in terminal (set listing to 0.0.0.0:8000 for device to connect to the web server)
    ```sh
    python manage.py runserver 0.0.0.0:8000
    ```
