from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from common.models import BaseModel
from apps.users.manager import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)

    class UserStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email