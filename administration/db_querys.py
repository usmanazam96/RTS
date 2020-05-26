from typing import Dict, Any, Union

from accounts.models import *


def admin_dashboard():
    user_count = User.objects.count()
    admin_count = Admin.objects.count()
    student_count = Student.objects.count()
    faculty_count = Faculty.objects.count()
    active_user = User.objects.filter(is_active=True).count()
    un_active_user = User.objects.filter(is_active=False).count()
    data = dict(user_count=user_count, admin_count=admin_count, student_count=student_count,
                faculty_count=faculty_count, active_user=active_user, un_active_user=un_active_user)
    return data
