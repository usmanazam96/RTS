"""RTS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List, Any

from django.contrib import admin
from django.urls import path
from meeting import views

app_name = 'meeting'

urlpatterns = [
    path("send/request/view/<int:id>/", views.send_meeting_request, name='send_request'),
    path("approve/meeting/<int:id>/", views.meeting_approve, name='approve_meeting'),
    path("reschedule/meeting/<int:id>/", views.meeting_reschedule, name='reschedule_meeting'),
    path("message/meeting/<int:id>/", views.meeting_message, name='message_meeting'),
    path("cancel/meeting/<int:id>/", views.meeting_cancel, name='cancel_meeting'),
    path("complete/meeting/<int:id>/", views.meeting_complete, name='complete_meeting'),
    # views
    path("request/faculty/views/", views.meeting_request_view_faculty, name='meeting_request_faculty_view'),
    path("reschdule/faculty/views/", views.meeting_reschedule_view_faculty, name='meeting_reschedule_faculty_view'),
    path("cancelled/faculty/views/", views.meeting_cancelled_view_faculty, name='meeting_cancel_faculty_view'),
    path("approve/faculty/views/", views.meeting_approve_view_faculty, name='meeting_approve_faculty_view'),
    path("complete/faculty/views/", views.meeting_complete_view_faculty, name='meeting_complete_faculty_view'),

    path("request/user/views/", views.meeting_request_view_user, name='meeting_request_user_view'),
    path("reschdule/user/views/", views.meeting_reschedule_view_user, name='meeting_reschedule_user_view'),
    path("cancelled/user/views/", views.meeting_cancelled_view_user, name='meeting_cancel_user_view'),
    path("approve/user/views/", views.meeting_approve_view_user, name='meeting_approve_user_view'),
    path("complete/user/views/", views.meeting_complete_view_user, name='meeting_complete_user_view'),

    # detail
    path("detail/meeting/view/<int:id>", views.meeting_detail_view_faculty, name='meeting_detail_faculty_view'),
    # detail
    path("detail/meeting/rview/<int:id>", views.meeting_detail_view_requester, name='meeting_detail_requester_view'),
]
