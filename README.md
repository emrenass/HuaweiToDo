# HuaweiToDo

 1. **Docker Installation**

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