# RECRUITMENT PORTAL

	* Practice problems
	* Participate in contests
	* Create questions
	* Host contests
	
# Key features

	* Authentication System - Login, Signup, Recovery, Email verification
	* Mailing Service
	* 3 user types - Standard, Setter, Admin
	* Problemset - Questions available for practice
	* Arena - Upcoming and Ongoing contests
	* Setter Portal - Apply to be a problem setter / host and manage contests. 
	* Admin Portal - Manage all contests and setter applications
	
# Snapshots

![scr1](https://github.com/dumbape/Recruitment-Portal/blob/master/ProblemSet.png?raw=true)
![scr2](https://github.com/dumbape/Recruitment-Portal/blob/master/Arena.png?raw=true)
![scr3](https://github.com/dumbape/Recruitment-Portal/blob/master/Contest.png?raw=true)
![scr4](https://github.com/dumbape/Recruitment-Portal/blob/master/Setter.png?raw=true)
![scr5](https://github.com/dumbape/Recruitment-Portal/blob/master/Challenge_Ended.png?raw=true)

# Install

1. Make sure to have pip installed. Install pip using: `sudo apt-get install pip`
2. (Optional) Switch to a virtual environment if you wish not to install required packages globally.
3. Open the terminal in current folder [in virtualenv] and type: `pip install -r requirements.txt`
4. After installing the packages, run the command: `python manage.py runserver`
5. Open the browser, goto the address: localhost:8000/
6. You may create a new account or login using an existing one (credentials are given below)
7. Goto the address: localhost:8000/admin and login with superuser credentials to change the user types to test the software.

# Credentials
`localhost:8000/login`

	1. dumbape
	2. parag_parihar
	3. pravin_01
	4. aashutosh_1
	5. aashutosh_2
	6. aashutosh_3
	7. pravin_01
	8. pravin_02

	Password for all users: 123456

# Superuser credentials
`localhost:8000/admin`

	1. dumbape

	Password: qwertyuiop
	
Alternatively, you may create a superuser using `python manage.py createsuperuser` and login using the new one too.

# Tools used

1. FrontEnd - HTML, CSS, JavaScript, JQuery
2. CSS Framework - Semantic UI
3. BackEnd - Python Django
4. Database - SQLite 3

	
