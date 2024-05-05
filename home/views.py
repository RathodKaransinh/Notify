import csv
import io
import json
import zipfile

from django.contrib.auth.decorators import permission_required, login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render

from home.forms import ItemForm
from .models import Item, Notice, NoticeKeyword


@login_required(login_url='/login/')
def list_notices(request):
    login_status = True
    if request.user.is_anonymous:
        login_status = False

    context = {
        'notices': Notice.objects.all(),
        'loginStatus': login_status,
        'user': request.user
    }

    return render(request, 'index.html', context)


@login_required(login_url='/login/')
@permission_required('home.add_notice')
def upload(request):
    if request.method == 'POST':
        title = request.POST['title']
        short_description = request.POST['short_description']
        file = request.FILES['file']
        notice = Notice.objects.create(title=title, short_description=short_description, file=file)
        notice.save()

    return render(request, 'upload.html')


@login_required(login_url='/login/')
def view_keywords(request):
    keywords = NoticeKeyword.objects.all()
    return render(request, 'view_keywords.html', {'keywords': keywords})


@login_required(login_url='/login/')
def add_items(request):
    ItemFormSet = modelformset_factory(Item, form=ItemForm, extra=1)
    if request.method == 'POST':
        formset = ItemFormSet(request.POST)
        delIndexes = json.loads(request.POST['deleted_forms'])
        if formset.is_valid():
            i = 0
            for form in formset:
                if str(i) not in delIndexes:
                    print(form.cleaned_data['title'], form.cleaned_data['keyword'], form.cleaned_data['quantity'])
                i += 1
        else:
            print(formset.errors)
    else:
        formset = ItemFormSet()

    return render(request, 'item_form.html', {'formset': formset})


def download(request):
    # Condition to determine file type (could be based on a query parameter, etc.)
    file_type = request.GET.get('type', 'error')

    print(file_type, type(file_type))

    if file_type == "type-csv":
        # Generate a CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]

        for row in data:
            writer.writerow(row)

        return response

    elif file_type == "type-zip":
        # Generate a ZIP file containing multiple CSV files
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zipf:
            # Example data for multiple CSV files
            files_data = [
                {"filename": "file1.csv", "data": [["Name", "Age"], ["Alice", 30]]},
                {"filename": "file2.csv", "data": [["Name", "Salary"], ["Bob", 50000]]},
            ]

            for file_data in files_data:
                file_buffer = io.StringIO()
                writer = csv.writer(file_buffer)

                for row in file_data["data"]:
                    writer.writerow(row)

                zipf.writestr(file_data["filename"], file_buffer.getvalue())

        response = HttpResponse(buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="data.zip"'

        return response

    else:
        return HttpResponse(status=300)
