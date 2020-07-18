from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render, redirect

from RTS.decorators import allowed_users
from accounts.forms import AdminForm
from administration.db_querys import *


# Create your views here.

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    context = dict(page_title='Admin-Dashboard', h1_title='Admin Dashboard', url='dashboard',
                   admin_home='active')
    context.update(admin_dashboard())
    return render(request, 'administration/index.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def profile(request):
    admin = request.user.admin
    context = dict(page_title='Admin-Profile', h1_title='Admin Profile', url='admin profile', admin=admin,
                   admin_profile_li='active', my_account_ul='menu-open')
    return render(request, 'administration/profile.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def edit_profile(request):
    admin = request.user.admin
    if request.method == "GET":
        form = AdminForm(instance=admin)
        context = dict(page_title='Administration-Profile Edit', h1_title='Edit Profile', url='editadmin',
                       card_title="Account Information", form=form,
                       admin_edit_profile_li='active', my_account_ul='menu-open')
        return render(request, 'administration/profile_form.html', context)
    else:
        updated = False
        form = AdminForm(data=request.POST, instance=admin, files=request.FILES)
        if form.is_valid():
            admin = form.save()
            updated = True
        if updated:
            messages.success(request, 'Account updated  Successfully')
            return redirect('administration:profile')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Administration-Profile Edit', h1_title='Edit Profile', url='editprofile',
                           card_title="Account Information", form=form,
                           admin_edit_profile_li='active', my_account_ul='menu-open')
            return render(request, 'administration/profile_form.html', context)
