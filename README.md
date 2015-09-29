# Senior-Independent-Work

## Quick Install Guide
First clone the repo
```
git clone https://github.com/jzuber4/Senior-Independent-Work.git
cd Senior-Independent-Work
```

Now we need to install all the dependencies for the project. First, make sure you have **easy_install** installed.
```
easy_install --version
```
This may print out something like `setuptools 3.3`.
If easy_install is not found, install it from your package manager or via: https://pypi.python.org/pypi/setuptools

Next, we need **virtualenv** and **pip**. virtualenv is a program that allows you to isolate your python installations
and their dependencies for each project. pip is a package manager that works well with virtualenv. 

Install virtualenv and pip
```
sudo easy_install virtualenv && 
sudo easy_install pip
```

Now set up the virtual environment
```
virtualenv venv
```
This will create a folder named *venv* in the project directory, where your dependencies can be installed.

Activate the virtual environment, which modifies your 
terminal to run python/pip/installed dependencies from the virtual environment.
```
source venv/bin/activate
```

You may notice your prompt changes to start with `(venv)` which indicates it is running in the virtual environment.
The virtual environment can be left any time by entering `deactivate`.

Now, install the dependencies with pip from the *requirements.txt* file.
```
pip install -r requirements.txt
```

Everything is now installed and the website can be fired up! But, the database has not yet been initialized.
This can be done with `manage.py` which is the main entry point for running and *managing* the Django website.
Make sure you are in the virtual environment whenever you're running `manage.py`, or else python might not be 
able to find the correct dependencies.

Set up the database.
```
python manage.py migrate
```

The website is now completely set up. Start it up!
```
python manage.py runserver
```

If all goes well, the server will start up successfully and report that it is running on `127.0.0.1:8000`. Type this
into your browser to visit the website.

Currently, the website requires a Princeton account to log in.
