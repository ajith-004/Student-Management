from django.shortcuts import render

# Create your views here.

from .models import Teacher, Student, StudentMark
from django.views.generic import View, FormView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class TeacherListView(View):

    def get(self, request):
        result = []
        teachers_obj = Teacher.objects.all()
        for teacher in teachers_obj:
            response = {
                "id": teacher.id,
                "name": teacher.name,
            }
            result.append(response)

        return JsonResponse(result, status=200, safe=False)


class StudentListView(View):

    def get(self, request):
        result = []
        student_obj = Student.objects.all()
        for student in student_obj:
            response = {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "gender": student.gender,
                "teacher": student.teacher.name
            }
            result.append(response)

        return JsonResponse(result, status=200, safe=False)


class StudentUpdateorCreateView(FormView):
    http_method_names = ["options", "put", "post"]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateorCreateView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        result = {}
        if not request.body:
            return self.get_error_response(
                {"message": "request body is empty"})
        request_body = json.loads(request.body)
        name = request_body.get("name")
        student_id = request_body.get('student_id')
        if not name:
            return self.get_error_response(
                {"message": "name is required"})
        teacher_name = request_body.get("teacher_name")
        if not teacher_name:
            return self.get_error_response(
                {"message": "teacher_name is required"})
        age = request_body.get("age")
        gender = request_body.get("gender")
        if request.method == "PUT":
            if not student_id:
                return self.get_error_response(
                    {"message": "student id is required"})
            try:
                teacher_obj = Teacher.objects.get(name=teacher_name)
                student_obj = Student.objects.get(id=student_id)
                student_obj.name = name
                student_obj.teacher_id = teacher_obj.id
                if age:
                    student_obj.age = age
                if gender:
                    student_obj.gender = gender
                student_obj.save()
            except Student.DoesNotExist:
                return self.get_error_response(
                    {"message": "Student does not exist"})
            except Teacher.DoesNotExist:
                return self.get_error_response(
                    {"message": "teacher does not exist"})
            result = {
                "status": "success",
                "result": "Student data updated successfully"
            }
        else:
            if not age:
                return self.get_error_response(
                    {"message": "age is required"})
            if not gender:
                return self.get_error_response(
                    {"message": "gender is required"})
            try:
                teacher_obj = Teacher.objects.get(name=teacher_name)
            except Teacher.DoesNotExist:
                return self.get_error_response(
                    {"message": "teacher does not exist"})

            student_exsist, created = Student.objects.get_or_create(
                name=name, age=age, gender=gender, teacher_id=teacher_obj.id
            )
            if not created:
                return self.get_error_response(
                    {"message": "student details already exsist"})
            result = {
                "status": "success",
                "result": "Student data created successfully"
            }
        return JsonResponse(result, status=200)

    def get_error_response(self, result, status=400):
        context = {"status": "error", "result": result}
        return JsonResponse(context, status=status)


class DeleteStudentView(FormView):
    http_method_names = ["options", "delete"]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(DeleteStudentView, self).dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        student_id = self.request.path.split('/')[3]
        try:
            student_obj = Student.objects.get(
                id=student_id)
            student_obj.delete()
        except Student.DoesNotExist:
            return self.get_error_response(
                {
                    "message": "Student id does not exist",
                })
        result = {
            "status": "success",
            "result": "Student deleted successfully"
        }
        return JsonResponse(result, status=200)

    def get_error_response(self, result, status=400):
        context = {"status": "error", "result": result}
        return JsonResponse(context, status=status)


class StudentMarkUpdateorCreateView(FormView):
    http_method_names = ["options", "put", "post"]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(StudentMarkUpdateorCreateView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        result = {}
        if not request.body:
            return self.get_error_response(
                {"message": "request body is empty"})
        request_body = json.loads(request.body)
        term = request_body.get("term")
        if not term:
            return self.get_error_response(
                {"message": "term is required"})
        student_id = request_body.get('student_id')
        maths = request_body.get("maths")
        if not maths:
            maths = 0
        science = request_body.get("science")
        if not science:
            science = 0
        history = request_body.get("history")
        if not history:
            history = 0
        total_marks = maths + science + history
        if request.method == "PUT":
            if not student_id:
                return self.get_error_response(
                    {"message": "student id is required"})
            try:
                studentmark_obj = StudentMark.objects.get(
                    student_id=student_id)
                studentmark_obj.term = term
                studentmark_obj.maths = maths
                studentmark_obj.science = science
                studentmark_obj.history = history
                studentmark_obj.total_marks = total_marks
                studentmark_obj.save()
            except StudentMark.DoesNotExist:
                return self.get_error_response(
                    {"message": "Student mark entry does not exist"})
            result = {
                "status": "success",
                "result": "Student mark data updated successfully"
            }
        else:
            student_exsist, created = StudentMark.objects.get_or_create(
                student_id=student_id, term=term, maths=maths, science=science,
                history=history, total_marks=total_marks
            )
            if not created:
                return self.get_error_response(
                    {"message": "student Marks details already exsist"})
            result = {
                "status": "success",
                "result": "Student Mark data created successfully"
            }
        return JsonResponse(result, status=200)

    def get_error_response(self, result, status=400):
        context = {"status": "error", "result": result}
        return JsonResponse(context, status=status)


class DeleteStudentMarkView(FormView):
    http_method_names = ["options", "delete"]

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(DeleteStudentMarkView, self).dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        student_mark_id = self.request.path.split('/')[3]
        try:
            student_mark_obj = StudentMark.objects.get(
                id=student_mark_id)
            student_mark_obj.delete()
        except StudentMark.DoesNotExist:
            return self.get_error_response(
                {
                    "message": "Student mark id does not exist",
                })
        result = {
            "status": "success",
            "result": "Student Mark deleted successfully"
        }
        return JsonResponse(result, status=200)

    def get_error_response(self, result, status=400):
        context = {"status": "error", "result": result}
        return JsonResponse(context, status=status)


class StudentMarkListView(View):

    def get(self, request):
        result = []
        studentmark_obj = StudentMark.objects.all()
        for student_mark in studentmark_obj:
            response = {
                "id": student_mark.student_id,
                "name": student_mark.student.name,
                "age": student_mark.term,
                "gender": student_mark.maths,
                "teacher": student_mark.science,
                "history": student_mark.history,
                "total_marks": student_mark.total_marks,
                "created_on": student_mark.created_at,
            }
            result.append(response)

        return JsonResponse(result, status=200, safe=False)
        