from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager): # 사용자 객체를 생성하고 관리하는 클래스
    def create_user(self, login_id, password=None): # 일반 사용자 생성
        if not login_id:
            raise ValueError("id는 필수입니다.")
        if not password:
            raise ValueError("비밀번호는 필수입니다.")
        
        user = self.model(login_id=login_id)
        user.set_password(password) # 비밀번호 해싱 처리
        user.save(using=self._db) # DB에 저장
        return user

    def create_superuser(self, login_id, password): # 관리자 생성
        # 일반 유저 생성 후 is_admin = True로 관리자 계정 생성
        user = self.create_user(
            login_id=login_id,
            password=password,
        )
        user.is_admin = True # 관리자 권한 부여
        user.save(using=self._db)
        return user


class User(AbstractBaseUser): # 실제 사용자 정보를 저장하는 모델 클래스
    login_id = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False) # 관리자 여부 (처음 생성시 false)
    objects = UserManager() # 기본 UserManager 대신 커스텀 UserManager(우리가 커스텀 한 class) 사용
    USERNAME_FIELD = 'login_id'

    def __str__(self):
        return self.login_id

    def has_perm(self, perm, obj=None): # 사용자가 특정 권한을 가지고 있는지 확인하는 메서드
        return True # 모든 권한 허용 (추후 수정 가능)

    def has_module_perms(self, app_label):
		    # 사용자가 특정 앱 내에서 하나 이상의 권한을 가지고 있는지 확인하는 메서드
        return True # 모든 앱에 접근 가능 (추후 수정 가능)
    
    class Meta:
        db_table = 'user' # 테이블명을 user로 설정 

class Profile(models.Model):
    # profile_id는 django에서 자동으로 만들어주는 pk
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30)
    job = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user_name
    
class Portfolio(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}의 포트폴리오"