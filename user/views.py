import json

from django.http import HttpResponse

from .models import User

def index(request):
    return HttpResponse("Hello, world!")

def register(request):
    new_user = None
    user = None
    if request.method == 'POST':
        new_user = json.loads(request.body)
        # print(new_user)
        username = new_user.get('username')
        password = new_user.get('password')
        # 这里继续添加用户注册需要的属性，邮箱等等
        # print(username, password)
        user = User.objects.create(username=username, password=password) # 这里添加向User表里insert需要的属性

    return HttpResponse(user)

def login(request):
    # username = None
    user = None
    if request.method == 'POST':
        user = json.loads(request.body)
# print(new_user)
        username = user.get('username')
        password = user.get('password')
        # 这里继续添加用户注册需要的属性，邮箱等等
        # print(username, password)
        getuser = User.objects.filter(username=username, password=password) # 这里添加向User表里insert需要的属性
        print(getuser)
        if not getuser.exists():
            return HttpResponse("failure")
    return HttpResponse("success") # 成功 or 失败
















