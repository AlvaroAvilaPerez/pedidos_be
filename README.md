# Installing Django and the Django REST Framework

This document will walk you through the process of installing Django and the Django REST Framework on your system. Be sure to follow the steps below to properly set up your development environment.

# Previous requirements

In console run the command

*** copy code ***
pip install -r requerimentes.text 

or

Python 3.6 or higher: Make sure you have Python installed on your system. You can check the python version by running the command in your terminal.

*** copy code ***
python --version 

# Installation

# Python installation:

- Go to the official Python website (https://www.python.org) and download the latest stable version for Windows.
- Run the downloaded file and check the "Add Python to PATH" option during installation.
- Click "Install Now" and wait for the installation to complete.

Creation of a virtual environment and activation:

- Open a command window (cmd) or PowerShell.

- Create a new folder for your project (you can choose any name and location).
- Navigate to the project folder using the cd command on the command line.
- Run the following command to create a virtual environment:

*** copy code ***
python -m venv myenv
(where "myenv" is the name you want to give your virtual environment).

- To activate the virtual environment, execute the following command:
copy code
myenv\Scripts\activate

# Django installation:

- Once the virtual environment is up, run the following command to install Django:

*** copy code ***
pip install django

# Django REST Framework Installation:

- Still with the virtual environment active, run the following command to install the Django REST Framework:

*** copy code ***
pip install djangorestframework

Deactivation of the virtual environment
- When you have finished working on your project, you can disable the virtual environment by running the following command:

*** copy code ***
deactivate

- This will take you back to your regular development environment.

That's all! You should now have Django and the Django REST Framework installed and ready to use on your system. Enjoy developing your web application!

# Additional features

# Installing Visual Studio Code:

- Go to the official website of Visual Studio Code (https://code.visualstudio.com) and download the installation file for Windows.
- Run the downloaded file and follow the installer instructions to complete the installation.

# Installing PyCharm:

- Go to the official PyCharm website (https://www.jetbrains.com/pycharm) and download the Community or Professional version according to your needs.
- Run the downloaded file and follow the installer instructions to complete the installation.

Postman Installation:
- Go to the official Postman website (https://www.postman.com) and download the Windows version.
- Run the downloaded file and follow the installer instructions to complete the installation.