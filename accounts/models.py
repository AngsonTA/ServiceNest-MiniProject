from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.



# Custom user manager to handle user and superuser creation
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)  # Hashes the password
        # user.is_active = True  # Set default status
        user.save(using=self._db)  # Saves to the database
        return user
    

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email= self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

         # Set superuser privileges
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Custom Account model
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)


    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

   # Login settings
    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Required when creating user via createsuperuser

    # Connect the custom manager
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    

     # Permissions handling
    def has_perm(self, perm, obj=None):
        return self.is_admin  # Admins have all permissions

    def has_module_perms(self, app_label):
        return True  # All users can view all app modules