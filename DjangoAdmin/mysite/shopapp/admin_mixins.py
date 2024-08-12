import csv

from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.db.models.options import Options


class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        print("=" * 200)
        meta: Options = self.model._meta
        field_names = [f"{field.name}\t" for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"

        csv_writer = csv.writer(response)
        csv_writer.writerow(field_names)

        for obj in queryset:
            csv_writer.writerow([f"{getattr(obj, field)}\t" for field in field_names])

        return response

    export_csv.short_description = "Export as CSV"


