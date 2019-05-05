# HuaweiToDo

 - **Docker Installation**

	 1. Clone Repo using `git clone https://github.com/emrenass/HuaweiToDo.git
	 2. Run command docker-compose up --build
	 3. 3 Services will installed 
		> web (contains Django Project which runs with gunicorn)
		> db (contains database)
		> Nginx (Nginx load balancer)
	 4. System does not have register function so every time docker-compose build runs, 3 user will be added to postgresql automatically which are
		> username: user1 password: pass
		> username: user2 password: pass
		> username: user3 password: pass
	 5. You can access to application from http://127.0.0.1:1337
 
 - **Standalone Installation**
	 If you do not want to use docker application can run directly with Django's builtin web server.
	 1. Clone Repo using `git clone https://github.com/emrenass/HuaweiToDo.git
	 2. Go to HuaweiToDo folder with "cd" command from terminal
	 3. Run these commands in order
		 - python manage.py makemigrations
		 - python manage.py migrate
		 - python mange.py collectstatic
		 - python manage.py runserver

 2.**Used Technologies**
 
	 1. Django with Python3.6
	 2. Bootstrap (For UI)
	 3. Docker (For DevOps)
	 4. Nginx (For Load-balancer)
	 5. Gunicorn (For Server)
	 6. PostgreSQL (For Database)
	 7. Jenkins (For testing as CI Tool)
 3.**Additional Notes**
	 - For import and export functions the application uses semicolon ";" separated csv files.

 
