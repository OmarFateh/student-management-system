admin hod:

    - name
    - email
    - password
    - phone
    - photo
    - address
    - gender
    - date of recruitment

    - login
    - add/view/remove student
    - add/view/remove staff
    - add/view/remove course
    - add/view/remove subject
    - view attendance data
    - view results data
    - add/view announcements
    - view/reply feedback
    - view assignments
    - logout

<!-- admin course:

    - phone
    - photo
    - address
    - gender
    - date of recruitment

    - login
    - add/view/remove student
    - add/view/remove staff
    - view attendance data
    - add/view announcements
    - view/reply feedback
    - view results data
    - logout -->

staff:

    - phone
    - photo
    - address
    - gender
    - date of recruitment

    - login
    - take student attendance
    - view attendance data
    - view profile
    - add/view results
    - add/view announcements
    - send feedback
    - add/view/download assignments
    - logout

student:

    - phone
    - photo
    - address
    - gender
    - courses
    - date of admission

    - login
    - view attendance
    - view profile
    - view/upload assignments
    - view results
    - view announcements
    - send feedback
    - logout

course:

    - name
    - code
    - admin hod
    - start date
    - end date

    - subject:
            - name
            - code
            - course
            - staff
            - start date
            - end date

attendance:

    - staff
    - course
    - subject
    - session year
    - attendance date

    - staff take/view/update/delete attendance data
    - student view attendance data
    - adminhod view attendance data   

feedback:
    
    - staff:
          - staff
          - content
          - reply
    
    - student:
          - staff
          - content
          - reply

    - staff add/view feedback
    - student add/view feedback
    - adminhod view/reply to staff/student feedback

results:

    - student 
    - subject 
    - session year
    - assignment no.1/2/3/4/5 marks
    - final exam marks
    
    - staff add/view/update results data
    - student view results data
    - adminhod view results data

announcement:

    - adminhod
    - staff
    - content
    - is_adminhod
    - is_staff

    - staff add/view announcement
    - adminhod add/view announcement
    - student view announcement

report:

    - student 
    - subject 
    - session year
    - report 
    - deadline date

    - staff add/view/update reports
    - student view/submit reports
    - adminhod view reports

contact:

    - view staff/students of the same course 
    -
    -

post:    

    - owner
    - image
    - content
    - comment:
            - reply
            - likes 
    - like 
    - favourite 
    - restrict comment
    
    - crud
    - comment
    - like 
    - favourite