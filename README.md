# Instagram Clone
> A student management system made with django framework.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [TODO](#TODO)


## Technologies
* Python 3.8
* Django 3.0.8
* Ajax
* JQuery

## Setup
The first thing to do is to clone the repository:  
`$ git clone https://github.com/OmarFateh/Instagram-Clone.git`  
Setup project environment with virtualenv and pip.  
`$ virtualenv project-env`  
Activate the virtual environment  
`$ source project-env/Scripts/activate`  
Install all dependencies  
`$ pip install -r requirements.txt`  
Run the server  
`py manage.py runserver`

## Features
* Authentication: Registeration, login, logout, change and reset password.

* Course Admin:  
      - add/view/remove student  
		  - add/view/remove staff  
      - view attendance data  
      - add/view announcements  
      - view/reply feedback  
      - view results data  

* Staff:  
      - take student attendance  
      - view attendance data  
      - view/update profile
      - add/view results  
      - add/view announcements  
    	- send feedback  
    	- add/view/download assignments  

* Student:
      - view attendance  
    	- view profile  
      - view/upload assignments  
      - view results  
      - view announcements  
      - send feedback  

* A user can contact and view profile of all staff and students, who share the same course.
* A user can add/update/delete a post to his community of the course.
* A user can like, add/update/delete a comment and a reply to a post in his community of the course.

## TODO
* Implement Direct Messages (DM)
