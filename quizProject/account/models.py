from django.db import models, IntegrityError

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, default='user')
    active = models.BooleanField(default=True)
    quiz_creator = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = BaseUserManager()


    def create_user(username, password):
        user = CustomUser(username=username, password=password)
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            return None

    def __str__(self):
        return f'Username: {self.username};\n Is_quiz_creator: {self.quiz_creator};'

    @property
    def get_username(self):
        return self.username

    @property
    def is_quiz_creator(self):
        return self.quiz_creator

    @property
    def is_active(self):
        return self.active