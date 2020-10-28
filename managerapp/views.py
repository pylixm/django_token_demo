import json
import hashlib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib import auth


class TokenRequireView(View):
    """
    获取header 数据
    - request.META.get("header key") 用于获取header的信息
    - 注意的是header key必须增加前缀HTTP，同时大写，例如你的key为username，那么应该写成：request.META.get("HTTP_USERNAME")
    - 另外就是当你的header key中带有中横线，那么自动会被转成下划线，例如my-user的写成： request.META.get("HTTP_MY_USER")
    """
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.filter(userprofile__token=request.META.get('HTTP_TOKEN')).first()
        if not user:
            return JsonResponse({
                'code': 403,
                'message': '认证不通过！'
            })
        return super().dispatch(request, *args, **kwargs)


## 注意顺序
class UserView(TokenRequireView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        message = []
        for user in users:
            message.append({
                'username': user.username,
                'telephone': user.userprofile.telephone
            })

        return JsonResponse({
            'code': 0,
            'message': message
        })


class LoginView(View):

    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pay_data = json.loads(request.body)
        username = pay_data.get('username')
        password = pay_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse({
                'code': 400,
                'message': '用户名或密码错误！'
            })
        else:
            # auth.login(request, user)
            # 生成token
            token = self.genarate_token(username)
            user.userprofile.token = token
            user.save()
            return JsonResponse({
                'code': 0,
                'message': '认证成功!',
                'token': token
            })

    def genarate_token(self, username):
        """
        生成token
        """
        return hashlib.md5(username.encode('utf-8')).hexdigest()