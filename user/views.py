import json

from django.http import HttpResponse
from .models import User
from .myforms import RegisterForm, UserForm


def register(request):
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

                # 创建新用户
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
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check form content"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password:  # 哈希值和数据库内的值进行比对
                    # request.session['is_login'] = True  # 往session字典内写入用户状态和数据
                    # request.session['user_id'] = user.id
                    # request.session['user_name'] = user.username
                    message = 'success'
                    response = {
                        'code': 200,
                        'message': message,
                        'data': {'username': user.username,
                                 'email': user.email,
                                 'id': user.id,
                                 'camera_urls': user.camera_urls}
                    }
                    return HttpResponse(json.dumps(response))
                else:
                    message = "username or password incorrect"
            except:
                message = "username or password incorrect"
        response = {
            'code': 403,
            'message': message,
            'data': None
        }
        return HttpResponse(json.dumps(response))
    # login_form = UserForm()
    response = {
        'code': 403,
        'message': 'please use post',
        'data': None
    }
    return HttpResponse(json.dumps(response))

def information(request, uid):
    if request.method == "GET":
        try:
            user = User.objects.get(id=uid) # select * from user where id=uid;
            response = {
                'code': 200,
                'message': 'success',
                'data': {'username': user.username,
                         'email': user.email,
                         'id': user.id,
                         'camera_urls': user.camera_urls}
            }
            return HttpResponse(json.dumps(response))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))
    return HttpResponse(json.dumps({'code': 403, 'message': 'please use get', 'data': None}))

def allinformation(request):
    if request.method == "GET":
        try:
            users = User.objects.all() # select * from user where id=uid;
            all_user_info = []
            for user in users:
                all_user_info.append({'id': user.id, 'username': user.username,
                                      'email': user.email, 'camera_urls': user.camera_urls})
            response = {
                'code': 200,
                'message': 'success',
                'data': all_user_info
            }
            return HttpResponse(json.dumps(response))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))
    return HttpResponse(json.dumps({'code': 403, 'message': 'please use get', 'data': None}))
