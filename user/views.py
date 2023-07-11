import json

from django.http import HttpResponse

from .models import User
from .myforms import RegisterForm


def index(request):
    return HttpResponse("Hello, world!")


def register(request):
    if request.session.get('is_login', None):  # 登录状态不允许注册
        response = {
            'code': 403,
            'message': 'cannot register when logged in',
            'data': None
        }
        return HttpResponse(response)
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "Two passwords are not the same"
                response = {
                    'code': 403,
                    'message': message,
                    'data': None
                }
                return HttpResponse(json.dumps(response))
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = 'the username has been used'
                    response = {
                        'code': 403,
                        'message': message,
                        'data': None
                    }
                    return HttpResponse(json.dumps(response))

                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = 'the email address has been used!'
                    response = {
                        'code': 403,
                        'message': message,
                        'data': None
                    }
                    return HttpResponse(json.dumps(response))

                # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create(username=username,
                                               password=password1,
                                               email=email)
                response = {
                    'code': 200,
                    'message': 'success',
                    'data': {'username': new_user.username,
                             'email': new_user.email,
                             'id': new_user.id}
                }
                return HttpResponse(json.dumps(response))
    # register_form = RegisterForm()
    response = {
        'code': 403,
        'message': 'please use post',
        'data': None
    }
    return HttpResponse(json.dumps(response))


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
        getuser = User.objects.filter(username=username, password=password)  # 这里添加向User表里insert需要的属性
        print(getuser)
        if not getuser.exists():
            return HttpResponse("failure")
    return HttpResponse("success")  # 成功 or 失败
