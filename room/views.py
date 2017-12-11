import json


from django.shortcuts import render,HttpResponse
from django.http import JsonResponse


from room import models
from room.forms import RegisterForm








# Create your views here.

def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})
    elif request.is_ajax():

        form = RegisterForm(request.POST)
        registerResponse = {"user": None, "error_list": None}

        if form.is_valid():
            form.save()
            registerResponse["user"] = form.cleaned_data.get("user")

        else:
            registerResponse["error_list"] = form.errors
        return HttpResponse(json.dumps(registerResponse))

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.is_ajax():

        state = {"state": None}
        username = request.POST.get("user")

        if username == "":
            state["state"] = "user_none"
            return HttpResponse(json.dumps(state))
        password = request.POST.get("pwd")

        if password == "":
            state["state"] = "pwd_none"
            return HttpResponse(json.dumps(state))

        user = models.User.objects.filter(user=username, pwd=password).first()

        if user:
            state["state"] = "login_success"
            request.session["username"] = user.user

            request.session["id"] = user.id


        else:
            state["state"] = "failed"

        return HttpResponse(json.dumps(state))

def index(request):
    if request.method == "GET":
        times = models.Time.objects.all()
        rooms = models.Room.objects.all()
        return render(request,'index.html',{"times":times,"rooms":rooms})
    elif request.is_ajax():
        state = {"error_list":None,"success":False,"user":None}
        data_list = json.loads(request.body.decode("utf-8"))
        user_id = request.session.get("id")
        print(user_id)



        for i in data_list:
            try:
                i["user_id"] = user_id
                order_obj = models.Order.objects.create(**i)
                state["success"] = True
                state["user"] = order_obj.user.user
                state["day"] = order_obj.day
            except Exception as e:
                print(e)
                state["error_list"] = "添加失败"
        return JsonResponse(state)

def booking(request):
    time_list = models.Time.objects.all()
    rooms = models.Room.objects.all()
    book_info = models.Order.objects.all()
    response = []
    for i in time_list:
        res = {}
        room_list = []
        # attrs =
        for room in rooms:

            room_list.append(room)

            res["attrs"] = {"room":room.id,"time_id":i.id}
            response.append(res)
    print(response)
    return HttpResponse("ok")



