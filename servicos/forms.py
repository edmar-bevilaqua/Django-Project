from django.forms import ModelForm
from .models import Services, Category
from django import forms

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    
    def __init__(self, *args, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(*args, **kwargs)

class ServiceForm(ModelForm):
    class Meta:
        model = Services
        exclude = ['finished', 'protocol', 'identifier']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding the Bootstrap class "form-control" and the placeholders for the items on the form
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})
            self.fields[field].widget.attrs.update({'placeholder':field})
            if (field == 'date_init') or (field == 'date_final'):
                self.fields[field].widget = DateTimeInput()
                self.fields[field].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        
        # Replacing the service tag with the service description
        choices = []
        for i, j in self.fields['service_category'].choices:
            service_category = Category.objects.get(title=j)
            choices.append((i.value, service_category.get_title_display()))
        
        self.fields['service_category'].choices = choices

