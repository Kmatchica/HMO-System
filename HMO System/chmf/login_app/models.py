from django.db import models
from department_app.models import department
from roles_app.models import roles
#######################################################



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    userid = models.IntegerField()
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    departmentcode = models.ForeignKey(department, on_delete=models.DO_NOTHING, to_field='departmentcode', blank=True)
    roleid = models.ForeignKey(roles, on_delete=models.DO_NOTHING, to_field='roleid', blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    street_address = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=300, blank=True)
    region = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=300, blank=True)
    barangay = models.CharField(max_length=300, blank=True)
    postal = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=300, blank=True)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'middle_name', 'last_name', 'contact_number','department','role','mobile_number','street_address','location','region','province','city','barangay','postal','status','remarks','transactby','transactdate','transactype' ]

    def __str__(self):
        return self.username
    

class historylogin(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno =  models.IntegerField()
     userid = models.IntegerField()
     username = models.CharField(max_length=100, blank=True)
     password = models.CharField(max_length=100, blank=True)
     first_name = models.CharField(max_length=100, blank=True)
     middle_name = models.CharField(max_length=100, blank=True)
     last_name = models.CharField(max_length=100, blank=True)
     email = models.EmailField(blank=True)
     departmentcode = models.ForeignKey(department, on_delete=models.DO_NOTHING, to_field='departmentcode', blank=True)
     roleid = models.ForeignKey(roles, on_delete=models.DO_NOTHING, to_field='roleid', blank=True)
     contact_number = models.CharField(max_length=20, blank=True)
     mobile_number = models.CharField(max_length=20, blank=True)
     street_address = models.CharField(max_length=300, blank=True)
     location = models.CharField(max_length=300, blank=True)
     region = models.CharField(max_length=300, blank=True)
     province = models.CharField(max_length=300, blank=True)
     city = models.CharField(max_length=300, blank=True)
     barangay = models.CharField(max_length=300, blank=True)
     postal = models.CharField(max_length=300, blank=True)
     status = models.CharField(max_length=300, blank=True)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historylogin"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='loginidh_idx'),
            
        ]    