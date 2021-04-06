from django.shortcuts import render

from posts.models import Post
from course.models import Subject
from student.models import Student
from posts.utils import paginate_posts
from posts.forms import CommentForm

def staff_posts(request):
    """
    Get posts of all staffs and students of current staff's courses, including current staff's posts.
    """
    # get list of all staffs' ids of current staff's courses.
    staff_ids_list = Subject.objects.staff_ids(request.user, is_staff=True)
    # get list of all courses' ids of current staff.
    courses_ids_list = Subject.objects.courses_ids(request.user)
    # get list of all students' ids of current staff's courses.
    students_ids_list = Student.objects.filter(course__id__in=courses_ids_list).values_list('user__id', flat=True)
    return Post.objects.feed(students_ids_list, staff_ids_list)

def staff_feed(request):
    """
    Display staff's feed.
    """
    # get staff's feed.
    posts = staff_posts(request)
    # paginate staff's feed.
    page_number = request.GET.get('page', 1)
    page_obj_posts = paginate_posts(posts, page_number)
    # comment form.
    comment_form = CommentForm(auto_id=False)  
    context = {'posts':page_obj_posts, 'comment_form':comment_form}
    return render(request, 'staff/staff_feed.html', context)