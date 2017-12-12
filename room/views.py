import json
from datetime import datetime

from django.shortcuts import render, HttpResponse
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
    times = models.Time.objects.all()

    return render(request, 'index.html', {"times": times})


def booking(request):
    """
    获取会议室预定情况以及预定会议室
    :param request:
    :param date:
    :return:
    """
    ret = {'code': 1000, 'msg': None, 'data': None}
    current_date = datetime.now().date()

    if request.method == "GET":
        try:
            fetch_date = request.GET.get('date')
            fetch_date = datetime.strptime(fetch_date, '%Y-%m-%d').date()
            if fetch_date < current_date:
                raise Exception('查询时间不能是以前的时间')

            booking_list = models.Order.objects.filter(day=fetch_date)


            booking_dict = {}
            for item in booking_list:
                if item.room_id not in booking_dict:
                    booking_dict[item.room_id] = {item.time_id: {'name': item.user.user, 'id': item.user_id}}
                else:
                    if item.time_id not in booking_dict[item.room_id]:
                        booking_dict[item.room_id][item.time_id] = {'name': item.user.user, 'id': item.user_id}
            """
            {
                room_id:{
                    time_id:{''},
                    time_id:{''},
                    time_id:{''},
                }
            }
            """

            room_list = models.Room.objects.all()

            booking_info = []
            for room in room_list:
                temp = [{'text': room.name, 'attrs': {'rid': room.id}, 'chosen': False}]
                for time in models.Time.objects.all():
                    v = {'text': '', 'attrs': {'time_id': time.id, 'room_id': room.id}, 'chosen': False}
                    if room.id in booking_dict and time.id in booking_dict[room.id]:
                        v['text'] = booking_dict[room.id][time.id]['name']
                        v['chosen'] = True
                        if booking_dict[room.id][time.id]['id'] != request.session.get('id'):
                            v['attrs']['disable'] = 'true'
                    temp.append(v)
                booking_info.append(temp)

            ret['data'] = booking_info
        except Exception as e:
            ret['code'] = 1001
            ret['msg'] = str(e)
        return JsonResponse(ret)

    elif request.is_ajax():
        state = {"error_list":None,"success":False,"user":None}
        data_list = json.loads(request.body.decode("utf-8"))

        user_id = request.session.get("id")




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
