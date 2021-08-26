from django.db import models

# Create your models here.

GENDER = (
    ('m', 'Male'),
    ('f', 'Female')
)

Term = (
    ('one', 'One'),
    ('two', 'Two')
)


class Teacher(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Student(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    age = models.IntegerField(default=15)
    gender = models.CharField(max_length=100, choices=GENDER, default='m')

    def __str__(self):
        return self.name


class StudentMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.CharField(max_length=100, choices=Term, default='one')
    maths = models.IntegerField(default=0)
    science = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.total_marks

        