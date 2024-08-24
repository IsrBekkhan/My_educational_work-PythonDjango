from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


def file_size_validate(file: InMemoryUploadedFile) -> None:
    if file.size > 1 * 1024 * 1024:
        raise ValidationError("Ошибка: файл больше 1 Мб не может быть отправлен!")


class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[file_size_validate])
