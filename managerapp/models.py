from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
自定义User的三种方法：
1. 使用OneToOneField 来扩展User的自动，权限及自带字段不动，侵入性最小；
2. 继承AbstractUser类，来自定义补充字段，需要修改settings配置AUTH_USER_MODEL;
3. 继承AbstractBaseUser类、PermissionsMixin类来实现，AbstractUser类中定义的自动都可以重新。这种对django侵入性最强，需要重新部分方法，
django的其他模块调用。该方式也需要修改settings配置AUTH_USER_MODEL;
4. 使用代理类来自定义User,这种方法不能自定义字段，但是可以自定义一些方法来获取需要的字段;

class ProxyUser(User):
    class Meta:
        proxy = True # 定义代理模型
    def get_data(self):
        return self.objects.filter("过滤条件")
"""


class UserProfile(models.Model):
    """创建一对一模型，并添加新的字段"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=11, verbose_name="手机号码", null=True, blank=True)
    token = models.CharField(max_length=50, verbose_name="token", null=True, blank=True)


# 监听到post_save事件且发送者是User则执行create_extension_user函数
@receiver(post_save, sender=User)
def create_extension_user(sender, instance, created, **kwargs):
    """
    使用信号来触发userprofile 的自定创建和保存
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()