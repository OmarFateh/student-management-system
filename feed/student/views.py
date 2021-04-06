from django.shortcuts import render

from posts.models import Post
from student.models import Student
from course.models import Subject
from posts.utils import paginate_posts
from posts.forms import CommentForm

def student_posts(request):
    """
    Get posts of all staffs and students of current student's course, including current student's posts.
    """
    # get list of all students' ids of current student's course.
    students_ids_list = Student.objects.filter(course=request.user.student.course).values_list('user__id', flat=True)
    # get list of all staffs' ids of current student's course.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_student=True)
    return Post.objects.feed(students_ids_list, staff_ids_list)

def student_feed(request):
    """
    Display student's feed.
    """
    # get student's feed.
    posts = student_posts(request) 
    # paginate student's feed.
    page_number = request.GET.get('page', 1)
    page_obj_posts = paginate_posts(posts, page_number)
    # comment form.
    comment_form = CommentForm(auto_id=False)
    context = {'posts':page_obj_posts, 'comment_form':comment_form}
    return render(request, 'student/student_feed.html', context)