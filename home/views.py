import csv
import io
import json
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelformset_factory, modelform_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

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


class BaseView(View):
    model_class = None
    form_class = None
    list_template_name = ''
    form_template_name = ''
    success_url = ''
    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('list_notices')
    permission_required = ''
    action = 'list'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)

        if not request.user.has_perm(self.permission_required):
            return redirect(self.redirect_url)

        if self.action == 'list':
            return self.list(request)
        elif self.action == 'create':
            return self.create(request)
        elif self.action == 'update':
            pk = kwargs.get('pk')
            if not pk:
                raise Http404("Update action requires a 'pk'.")
            return self.update(request, pk)
        elif self.action == 'delete':
            pk = kwargs.get('pk')
            if not pk:
                raise Http404("Delete action requires a 'pk'.")
            return self.delete(request, pk)
        else:
            raise Http404("Unknown action.")

    def list(self, request):
        queryset = self.model_class.objects.all()
        return render(request, self.list_template_name, {'queryset': queryset})

    def create(self, request):
        if request.method == 'POST':
            form = self.form_class(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, self.model_class.__name__ + " created successfully.")
                return redirect(self.success_url)
            else:
                messages.error(request, "There was an error with your submission.")
        else:
            form = self.form_class()

        return render(request, self.form_template_name, {'form': form})

    def update(self, request, pk):
        item = get_object_or_404(self.model_class, pk=pk)

        if request.method == 'POST':
            form = self.form_class(data=request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, self.model_class.__name__ + " updated successfully.")
                return redirect(self.success_url)
            else:
                messages.error(request, "There was an error with your submission.")
        else:
            form = self.form_class(instance=item)

        return render(request, self.form_template_name, {'form': form})

    def delete(self, request, pk):
        item = get_object_or_404(self.model_class, pk=pk)
        item.delete()
        messages.success(request, self.model_class.__name__ + " deleted successfully.")
        return redirect(self.success_url)


class KeywordCrudView(BaseView):
    model_class = NoticeKeyword
    form_class = modelform_factory(NoticeKeyword, fields='__all__')
    list_template_name = 'list_keywords.html'
    form_template_name = 'keyword_form.html'
    success_url = reverse_lazy('list_keywords')

