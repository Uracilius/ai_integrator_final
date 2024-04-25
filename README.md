# Name: BEAM

## Description

This project is a modular virtual assistant that incorporates various concepts learned from the AI Integrator course. It aims to create a virtual assistant that remembers more than just the user's name and can perform various tasks based on user interactions.
## Setup Instructions:

### Install Dependencies:
Before running the project, ensure that you have all the required dependencies installed. You can do this by running the following command in your terminal or command prompt:

~~~bash
$ pip install -r requirements.txt
~~~

### Setup ChromaDB Database:
The project utilizes ChromaDB as its database. You need to set up a ChromaDB database and configure its connection details in the config.json file located at 

~~~bash
src/modules/face_recognition/src/db/config.json
~~~

Ensure you input the correct database connection details, including the port number.

# Run the Project:
Once you have installed the dependencies and configured the database, you can run the entire project using the main module controller. Navigate to the project directory and run the following command:
~~~bash
$ python -m src.modules.main_controller
~~~