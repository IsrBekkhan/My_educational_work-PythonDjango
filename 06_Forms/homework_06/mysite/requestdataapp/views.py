from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile

from .forms import FileUploadForm


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")


def upload_form(request: HttpRequest) -> HttpResponse:
    context = dict()

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            my_file = form.cleaned_data["file"]

            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)
            print("file_name:", file_name)
            context["status"] = "Файл успешно отправлен!"
    else:
        form = FileUploadForm()

    context["form"] = form

    return render(request, "requestdataapp/file-upload-form.html", context=context)

