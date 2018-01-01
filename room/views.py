import json
import hashlib
from datetime import datetime

from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from django.db.models import Q

from room import models
from room.forms import RegisterForm


# Create your views here.
def md5(val):
    '''
    加密 密码
    :param val:
    :return:
    '''
    m = hashlib.md5()
    m.update(val.encode('utf-8'))
    return m.hexdigest()

def auth(func):
    '''
    登录装饰器
    :param func:
    :return:
    '''
    def inner(request,*args,**kwargs):
        user_info = request.session.get("user_info")
        if not user_info:
            return redirect("/login/")
        return func(request,*args,**kwargs)
    return inner

def auth_json(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get("user_info")
        if not user_info:
            return JsonResponse({"status":False,"msg":"用户未登录"})
        return func(request,*args,**kwargs)
    return inner


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})
    elif request.is_ajax():

        form = RegisterForm(request.POST)
        registerResponse = {"user": None, "error_list": None}

        if form.is_valid():
            form.cleaned_data["pwd"] = md5(form.cleaned_data["pwd"])
            pwd = form.cleaned_data["pwd"]
            user = form.cleaned_data["user"]
            phone = form.cleaned_data["phone"]
            models.User.objects.create(user=user,pwd=pwd,phone=phone)
            registerResponse["user"] = form.cleaned_data.get("user")

        else:
            registerResponse["error_list"] = form.errors
        return HttpResponse(json.dumps(registerResponse))


def login(request):
    '''
    登录
    :param request:
    :return:
    '''
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

        user = models.User.objects.filter(user=username, pwd=md5(password)).first()

        if user:
            state["state"] = "login_success"
            request.session["user_info"] = {"username":user.user,"id":user.id}

        else:
            state["state"] = "failed"

        return HttpResponse(json.dumps(state))

@auth
def index(request):
    times = models.Time.objects.all()

    return render(request, 'index.html', {"times": times})

@auth_json
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
        try:
            fetch_date = request.POST.get('date')
            fetch_date = datetime.strptime(fetch_date, '%Y-%m-%d').date()
            if fetch_date < current_date:
                raise Exception('不能是以前的时间')
            book_info = json.loads(request.POST.get("data"))

            for room_id,time_id_list in book_info["ADD"].items():


                if room_id not in book_info["DEL"]:
                    continue
                else:
                    for time_id in list(time_id_list):
                        if time_id in book_info["DEL"][room_id]: #取到删除字典中的time_id判断增加的time_id是否在其中
                            book_info["DEL"][room_id].remove(time_id)#说明这个是不打算删掉的
                            book_info["ADD"][room_id].remove(time_id)


            add_book_list = []

            for room_id, time_id_list in book_info["ADD"].items():
                for time_id in time_id_list:
                    order_obj = models.Order(
                        user_id = request.session.get("id"),
                        room_id = room_id,
                        time_id = time_id,
                        day = fetch_date
                    )
                    add_book_list.append(order_obj)
            models.Order.objects.bulk_create(add_book_list)

            #取消预定的
            removing_book = Q()
            for room_id,time_id_list in book_info["DEL"].items():
                for time_id in time_id_list:
                    tem = Q()
                    tem.connector = 'AND' #且的关系
                    tem.children.append(("user_id",request.session.get("id")))
                    tem.children.append(("room_id",room_id))
                    tem.children.append(("time_id",time_id))
                    tem.children.append(("day",fetch_date))

                    removing_book.add(tem,"OR")#或的关系

            if removing_book:
                models.Order.objects.filter(removing_book).delete()

        except Exception as e:
            ret["code"] = 1001
            ret["msg"] = str(e)

        return JsonResponse(ret)
