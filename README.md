# Heatstroke-Project
## Getting Started
You have to install software before using the project.
1. Download [Python](https://www.python.org/downloads/)
2. Install [Visual Studio Code](https://code.visualstudio.com/download)


### Installation
1. Clone the repo
    ```sh
    git clone https://github.com/6310611030/Heatstroke-Project
    ```
2. Open the dirctory with Visual Studio Code
   ```sh
    code .
    ```
3. Change directory to the project
    ```sh
    cd Heatstroke-Project/Heatstroke/heatstroke_warning_system
    ```
4. Set Up a Virtual Environment (Optional but Recommended)
    ```sh
    python -m venv .venv
    ```
5. Activate the virtual environment
   ```sh
    .venv\Scripts\activate
    ```
6. Install requirements for the project
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1. Migrate 
    ```sh
    python manage.py migrate 
    ```
1. Create a Superuser
    ```sh
    python manage.py createsuperuser
    ```

### Device library
1. SparkFun_MAX3010x_Sensor_Library
2. DHT-sensor-library by Adafruit
3. Adafruit-MLX90614-Library
   
