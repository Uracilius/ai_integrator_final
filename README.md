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
The project utilizes ChromaDB, PostgreSQL and MongoDB as its' storage. You need to set them up and and configure their connection details in the config.json file located at 

~~~bash
src/modules/face_recognition/src/db/config.json
~~~

Ensure you input the correct database connection details, including the port number.

# Run the Project:
Once you have installed the dependencies and configured the database, you can run the entire project using the main module controller. Navigate to the project directory and run the following command:
~~~bash
$ python -m src.modules.main_controller
~~~

# Feature creep list:
1) Custom face embedding model
2) Normalization of face input for more accurate recognition results\
3) Cleaned up error handling to be only on lowest levels
4) Vital/Priority conversations(for future fine-tuning of OPENAI model)
5) Independent summary processed for context(go over mongo database and see if any context is over 1k tokens. If yes - summarize.)
6) Add fine-tuning logic for the future( get all "vital" or important tags with high priortity and format them for fine-tuning CHATGPT)