from django import forms
from .models import Item, NoticeKeyword

class ItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Add a Bootstrap-like class
                'placeholder': f'Enter {field_name}',  # Add a placeholder
            })
    
    class Meta:
        model = Item
        fields = ['title', 'keyword', 'quantity']
