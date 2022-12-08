import pywhatkit as pwk
from datetime import datetime
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from trainer_app.models import Course, City, Trainer_Reg, Batch_Assign



def register_fun(request):
    city_data = City.objects.values()
    course_data = Course.objects.values()
    data = {
        'city': city_data,
        'course': course_data,
        'data1': ''
    }
    return render(request, 'register.html', data)

def reg_data_fun(request):
    username = request.POST['txtN']
    userage = request.POST['txtA']
    userphone = request.POST['txtPH']
    userpassword = request.POST['txtP']
    usermail = request.POST['txtM']
    usercity = request.POST['ddlCity']
    usercourse = request.POST['ddlCourse']
    usertype = request.POST['txtUT']
    if usertype == 'Admin':
        u1 = User.objects.create_superuser(username= username, password=userpassword, email=usermail)
        u1.save()
        return redirect('login')
    elif usertype == 'Trainer':
        t1 = Trainer_Reg()
        t1.Tname = username
        t1.Tage = userage
        t1.Tphone = userphone
        t1.Temail = usermail
        t1.Tpassword = userpassword
        t1.Tcity = City.objects.get(city_name=usercity)
        t1.Tcourse = Course.objects.get(course_name=usercourse)
        t1.save()
        return redirect('login')
    else:
        return redirect('register', {'data1': 'enter proper data'})


def log_fun(request):
    return render(request, 'login.html', {'data': ''})

def log_data_fun(request):
    user_name = request.POST['txtN']
    user_password = request.POST['txtP']
    user1 = authenticate(username=user_name, password=user_password)
    if user1 is not None:
        if user1.is_superuser:
            u1 = User.objects.get(username=user_name)
            request.session['user1'] = u1.id
            return render(request, 'admin//admin_home.html', {'data': u1.username})
    elif Trainer_Reg.objects.filter(Tname=user_name, Tpassword=user_password).exists():
        t1 = Trainer_Reg.objects.get(Tname=user_name)
        request.session['user2'] = t1.id
        return render(request, 'trainer//trainer_home.html', {'data': t1.Tname})
    else:
        return render(request, 'login.html', {'data': 'credentials are not correct...'})



# ----------------------------------------------------
#               admin module
# ----------------------------------------------------


def admin_home_fun(request):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    return render(request, 'admin//admin_home.html', {'data': u1.username})


def trainer_details_fun(request):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    t1 = Trainer_Reg.objects.all()
    return render(request, 'admin//trainer_details.html', {'data': t1})

def delete_fun(request, id):
    t1 = Trainer_Reg.objects.get(id=id)
    t1.delete()
    return redirect('trainer_details')


def batch_assign_fun(request):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    t1 = Trainer_Reg.objects.all()
    c1 = Course.objects.values()
    return render(request, 'admin//batch_asign.html', {'data1': t1, 'data2': c1})

def batch_assign_data_fun(request):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    ba = Batch_Assign()
    ba.Trainer_Name = Trainer_Reg.objects.get(Tname=request.POST['ddlN'])
    ba.Batch_No = request.POST['txtBN']
    ba.Date = request.POST['txtD']
    ba.Trainer_Course = Course.objects.get(course_name=request.POST['ddlC'])
    ba.save()

    # below code is for sending the whatsapp msg
    c1 = Course.objects.get(course_name=request.POST['ddlC'])       # course details
    t = Trainer_Reg.objects.get(Tname=request.POST['ddlN'])         # trainer details
    s = f'{ba.Batch_No} and course {c1.course_name} starts from {ba.Date}'
    s1 = f'+91{t.Tphone}'

    now = datetime.now()
    hour = int(now.strftime('%H'))
    min = int(now.strftime('%M'))

    pwk.sendwhatmsg(s1, f"hii {t.Tname} you are having a new batch No {s}", hour, min+1)
    return redirect('batch_details')

def batch_details_fun(request):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    bd = Batch_Assign.objects.all()
    return render(request, 'admin//batch_details.html', {'data': bd})

def batch_update_fun(request, id):
    u1 = User.objects.get(id=request.session['user1'])          # this code is used in all functions for the loging out
    ba = Batch_Assign.objects.get(id=id)

    t1 = Trainer_Reg.objects.values()
    c1 = Course.objects.values()
    if request.method == 'POST':
        ba.Trainer_Name = Trainer_Reg.objects.get(Tname=request.POST['ddlN'])
        ba.Batch_No = request.POST['txtBN']
        ba.Date = request.POST['txtD']
        ba.Trainer_Course = Course.objects.get(course_name=request.POST['ddlC'])
        ba.save()

        # below code is for sending the whatsapp msg
        c1 = Course.objects.get(course_name=request.POST['ddlC'])  # course details
        t = Trainer_Reg.objects.get(Tname=request.POST['ddlN'])  # trainer details
        s = f'{ba.Batch_No} and course {c1.course_name} starts from {ba.Date}'
        s1 = f'+91{t.Tphone}'

        now = datetime.now()
        hour = int(now.strftime('%H'))
        min = int(now.strftime('%M'))

        pwk.sendwhatmsg(s1, f"hii {t.Tname} your assigned batch has been updated as {s}", hour, min+1)

        # pwk.sendwhatmsg(phone, "hi", 10, 43)      # this code will send the whatsapp message when this fun will executed
        return redirect('batch_details')
    return render(request, 'admin//batch_update.html', {'data1': t1, 'data2': c1, 'data': ba})

def batch_delete_fun(request, id):
    ba = Batch_Assign.objects.get(id=id)
    ba.delete()
    return redirect('batch_details')



# ----------------------------------------------------
#               trainer module
# ----------------------------------------------------

def trainer_home_fun(request):
    t1 = Trainer_Reg.objects.get(id = request.session['user2'])                     # this code is used in all functions for the loging out
    return render(request, 'trainer//trainer_home.html', {'data': t1.Tname})

def tbatch_details_fun(request):
    t1 = Trainer_Reg.objects.get(id=request.session['user2'])                        # this code is used in all functions for the loging out
    # bd = Batch_Assign.objects.filter(Trainer_Name=request.session['user2'])        # we can use this code instead of below one
    bd = Batch_Assign.objects.filter(Trainer_Name=Trainer_Reg.objects.get(Tname=t1.Tname))
    return render(request, 'trainer//batch_details.html', {'data': bd})

def trainer_Details_fun(request):
    t1 = Trainer_Reg.objects.get(id=request.session['user2'])                        # this code is used in all functions for the loging out
    return render(request, 'trainer//trainer_Details.html', {'data': t1})

def trainer_update_fun(request, id):
    t1 = Trainer_Reg.objects.get(id=request.session['user2'])                       # this code is used in all functions for the loging out
    c1 = City.objects.values()
    c2 = Course.objects.values()
    if request.method == 'POST':
        t1.Tname = request.POST['txtN']
        t1.Tphone = request.POST['txtPH']
        t1.Temail = request.POST['txtM']
        usercity = request.POST['ddlCity']
        t1.Tcity = City.objects.get(city_name=usercity)
        usercourse = request.POST['ddlCourse']
        t1.Tcourse = Course.objects.get(course_name=usercourse)
        t1.save()
        return redirect('Trainer_details')
    return render(request, 'trainer//trainer_update.html', {'data': t1, 'data2': c1, 'data3': c2})

# ----------------------------------------------------
#          logout for both admin and trainer
# ----------------------------------------------------

def logout_fun(request):
    auth.logout(request)
    # return redirect('login')
    return render(request, 'login.html', {'data': 'successfully logged out...'})