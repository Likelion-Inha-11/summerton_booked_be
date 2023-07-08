from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,User

class MyUserManager(BaseUserManager):
    def create_user(self, userID, password=None, **extra_fields):
        if not userID:
            raise ValueError('The User ID must be set')
        extra_fields.setdefault('password', make_password(password))  # 비밀번호 암호화
        user = self.model(userID=userID, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(userID, password, **extra_fields)

class Profile(AbstractBaseUser):
    userID = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=15)
    user_mbti = models.CharField(max_length=4)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)  # 새로 추가된 user 필드


    # 필요한 추가 필드를 여기에 추가할 수 있습니다.

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'userID'
    # 필요한 경우 추가 필드를 USERNAME_FIELD로 설정할 수 있습니다.
    # 예: USERNAME_FIELD = 'email'

    def __str__(self):
        return self.nickname
    
    def has_perm(self, perm, obj=None):
        # 필요한 경우 권한 체크 로직을 구현합니다.
        # 예를 들어, 특정 권한을 가진 사용자인지 확인하는 로직을 작성합니다.
        return True  # 예시로 모든 사용자에게 권한을 부여함

    def has_perms(self, perm_list, obj=None):
        # 필요한 경우 다중 권한 체크 로직을 구현합니다.
        # 예를 들어, 여러 개의 권한 중 하나라도 가지고 있는지 확인하는 로직을 작성합니다.
        return True  # 예시로 모든 사용자에게 권한을 부여함
    
    def has_module_perms(self, app_label):
        return self.is_staff
