from django.db import models

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name

class City(models.Model):
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name

class Trainer_Reg(models.Model):
    Tname =  models.CharField(max_length=50)
    Tage = models.IntegerField()
    Tphone = models.BigIntegerField()
    Temail = models.EmailField(max_length=50)
    Tpassword = models.CharField(max_length=50)
    Tcity = models.ForeignKey(City, on_delete=models.CASCADE)
    Tcourse = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        # return f'{self.Tname},{self.Tage}'        we can return mutiple values like this
        return f'{self.Tname}'

class Batch_Assign(models.Model):
    Trainer_Name = models.ForeignKey(Trainer_Reg, on_delete=models.CASCADE)
    Batch_No = models.IntegerField()
    Date = models.DateTimeField()
    Trainer_Course = models.ForeignKey(Course, on_delete=models.CASCADE)

