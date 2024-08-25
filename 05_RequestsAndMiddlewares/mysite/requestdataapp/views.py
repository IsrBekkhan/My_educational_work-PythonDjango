from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")


def upload_form(request: HttpRequest) -> HttpResponse:
    context = dict()
    if request.method == "POST" and request.FILES.get("my_file"):
        my_file: TemporaryUploadedFile = request.FILES["my_file"]

        if my_file.size > 1 * 1024 * 1024:
            context["status"] = "Ошибка: файл больше 1 Мб не может быть отправлен!"
        else:
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)
            print("file_name:", file_name)
            context["status"] = "Файл успешно отправлен!"

    return render(request, "requestdataapp/file-upload-form.html", context=context)

