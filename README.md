# Student Management System
> A student management system made with django framework and JS.

## Table of contents
* [Technologies](#technologies)
* [Live](#live)
* [Features](#features)
* [User Credintials](#User-Credintials)
* [TODO](#TODO)

## Technologies
* Python 3.8
* Django 2.2.19
* Ajax
* JQuery
* Chart.js

## Live
https://student-m-s.herokuapp.com/

## Features
* Authentication: Registration, login(with email), logout, change and reset password.

* Course Admin:  
      - add/view/remove student  
      - add/view/remove staff  
      - When course admin adds student or staff, they get a random password, and in the first time they log in, they will get redirected to change their passwords.     
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
* A user can search, filter and paginate all the data.
* A user can add/update/delete a post to his community of the course.
* A user can like, add/update/delete a comment and a reply to a post in his community of the course.
* A user can view his notifications

## User Credintials
* Admin(Mathematics admin): - email--> ahmadmohamad@gmail.com  - password-->admin1600  
* Staff(Algebra teacher): - email--> omarali@gmail.com  - password-->admin1600  
* Student: - email--> ahmadali@gmail.com  - password-->admin1600

## TODO
* Implement Direct Messages (DM)
