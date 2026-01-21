from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Employee

User = get_user_model()

class PhoneOrUsernameBackend(ModelBackend):
    """
    自定义认证后端：支持使用 用户名 或 手机号 登录
    [修复版]：解决同一个手机号对应多个员工时报错的问题
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        
        user = None
        # 1. 尝试通过标准 用户名 (username) 查找
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 2. 如果用户名找不到，尝试通过 员工手机号 (phone) 查找
            # [关键修改] 使用 filter().first() 代替 get()
            # 这样即使数据库里有 3 个相同的手机号，也只会取第一个，不会报错崩溃
            employee = Employee.objects.filter(phone=username).first()
            
            if employee:
                # 获取该员工关联的 User 账号
                user = employee.user
            else:
                # 手机号也找不到
                return None

        # 3. 校验密码
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
            
        return None