# HuaweiToDo

 1. **Docker Installation**

	 1. Clone Repo using `git clone https://github.com/emrenass/HuaweiToDo.git
	 2. Run command docker-compose up --build
	 3. 3 Services will installed 
		- web (contains Django Project which runs with gunicorn)
		- db (contains database)
		- Nginx (Nginx load balancer)
	 4. System does not have register function so every time docker-compose build runs, 3 user will be added to postgresql automatically which are
		- username: user1 password: pass
		- username: user2 password: pass
		- username: user3 password: pass
	 5. You can access to application from http://127.0.0.1:1337
 
 2. **Standalone Installation**
	 If you do not want to use docker, the application can run directly with Django's builtin web server.
	 1. Clone Repo using `git clone https://github.com/emrenass/HuaweiToDo.git
	 2. Go to HuaweiToDo folder with "cd" command from terminal
	 3. Run these commands in order
		 - `python manage.py makemigrations`
		 - `python manage.py migrate`
		 - `python mange.py collectstatic`
		 - `python manage.py runserver`
	 4. Since standalone installation does not contain script for first start, and application does not have register method, a user must be created with following command
	 5. `python manage.py createsuperuser --username=joe --email=joe@example.com`

 3. **Backend Deployment Diagram**
	 ![enter image description here](https://raw.githubusercontent.com/emrenass/HuaweiToDo/master/HuaweiToDo.png)

 3.**Used Technologies**
 
	 1. Django with Python3.6
	 2. Bootstrap (For UI)
	 3. Docker (For DevOps)
	 4. Nginx (For Load-balancer)
	 5. Gunicorn (For Server)
	 6. PostgreSQL (For Database)
	 7. Jenkins (For testing as CI Tool)
 
 4.**How To Use**
 Login to system with user credentials given above.
 Create ToDo either with create button or import button which accept semicolon separated csv file
 For updating todo click either complete/not complete button to change status, or delete button to delete todo
 
 5.**Additional Notes**
	 - For import and export functions the application uses semicolon ";" separated csv files.
	 - Jenkins config can be found in this repo

 
