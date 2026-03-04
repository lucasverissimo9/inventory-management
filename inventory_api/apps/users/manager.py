from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if email is None:
            raise ValueError("The email is a required field")

        email = self.normalize_email(email=email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        self.extra_fields.setdefault("is_staff", True)
        self.extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password)
    

    