from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.core.mail import EmailMessage
import jwt
from .models import Jobs, extended
import random
from faker import Faker

fake = Faker()


def fake_data(request):
    obj = Jobs()

    job_list = []

    for _ in range(50):
        job = {
            "title": fake.job(),
            "description": fake.text(max_nb_chars=100),
            "amount": round(random.uniform(20.0, 500.0), 2),
            "status": random.choice(["Open", "In Progress", "Completed"]),
            "date": fake.date_between(start_date="-30d", end_date="today").strftime("%Y-%m-%d")
        }

        job_list.append(job)

    for data in job_list:
        Jobs.objects.create(
            title=data['title'],
            description=data['description'],
            amount=data['amount'],
            status=data['status'],
            date=data['date']
        )

    return HttpResponse("Fake Data inserted in Jobs Model")


@login_required(login_url='my_login')
def home(request):
    # if request.user.is_authenticated:
        obj = Jobs.objects.all()
        # import pdb;pdb.set_trace()
        return render(request, 'home.html', {'username': request.user.username,'profile_image': image,'ob': obj})


obj = Jobs.objects.all()
image = extended.objects.all()

# else:
#     return render(request, 'login.html')

# obj = Jobs.objects.all()
# return render(request, 'home.html', {'ob': obj})


def delete(request, id):
    obj = Jobs.objects.get(pk=id)
    try:
        obj.delete()
        return redirect(reverse("home"),{'ob':obj})
    except:
        return HttpResponse("Job not existed")


from datetime import datetime

def edit(request, id):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        amount = request.POST['amount']
        status = request.POST['status']
        date = request.POST['date']
        obj = Jobs.objects.get(pk=id)
        obj.title = title
        obj.description = description
        obj.amount = amount
        obj.status = status
        # date_ob = datetime.strptime(date, "%b. %d, %Y")
        # for_date = date_ob.strftime("%Y-%m-%d")
        # obj.date = for_date
        obj.save()
        try:

            obj = Jobs.objects.all()
            return render(request,'home.html',{'ob': obj})
        except:
            return HttpResponse("Network issue...")
    obj = Jobs.objects.get(pk=id)
    return render(request, 'edit.html', {'ob': obj})


# import pdb;pdb.set_trace():

def my_login(request):
    if request.method == 'POST':
        usern = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username=usern, password=passw)
        if user is not None:
            login(request, user)
            return render(request, 'home.html', {'username': usern, 'ob':obj})
        else:
            return render(request, 'login.html', {'msg': "Wrong Credentials."})
    return render(request, 'login.html')


def my_logout(request):
    logout(request)
    return render(request, 'login.html')


def my_signup(request):
    if request.method == "POST":
        new_username = request.POST['nam']
        new_email = request.POST['emai']
        new_password = request.POST['passwor']
        im = request.FILES['imageFile']
        # for email authentication => is_active=False
        user = User.objects.create_user(username=new_username, email=new_email, password=new_password, is_active=True)
        try:
            user.save()
            ex = extended()
            ex.id = user
            ex.img = im
            ex.save()
            encode = jwt.encode({'myid': str(user.pk)}, key="secret", algorithm='HS256')
            # link = 'http://127.0.0.1:8000/activation/'+str(user.pk)+'/' never use hardcore url address
            link = request.scheme + '://' + request.META['HTTP_HOST'] + '/activation/' + str(encode) + '/'
            em = EmailMessage("Account Activation", "Thanks for Registeration....!\n" + link, "garrison18552gmail.com",[new_email])
            em.send()
            return render(request, 'login.html', {'msg': 'user created successfully!'})
        except:
            return render(request, 'signup.html', {'msg': 'Network Error!!'})
    return render(request, 'signup.html')


def activation(request, id):
    decode = jwt.decode(id, key='secret', algorithms=['HS256'])
    us = User.objects.get(pk=int(decode['myid']))
    us.is_active = True
    us.save()
    return render(request, 'login.html', {'msg': 'Account Activated Successfully....!'})
