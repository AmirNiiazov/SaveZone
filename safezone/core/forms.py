from django import forms
from django.forms import CheckboxInput
from .models import Facilities, Devices, AccessPasses


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = ['title', 'location', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = ['title', 'facility', 'is_active', 'description', 'api_url', 'api_token']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class AccessPassForm(forms.ModelForm):
    class Meta:
        model = AccessPasses
        fields = ['full_name', 'valid_from', 'valid_to', 'note', 'facility', 'device']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

        if user.role == 'admin':
            self.fields['facility'].widget = forms.HiddenInput()
            self.fields['facility'].initial = user.facility
            self.fields['facility'].label = ''
            self.fields['device'].queryset = Devices.objects.filter(facility=user.facility, is_active=True)

        else:
            self.fields['facility'].queryset = Facilities.objects.all()
            self.fields['device'].queryset = Devices.objects.filter(is_active=True)
            # добавим id для js
            self.fields['facility'].widget.attrs.update({'id': 'id_facility'})
            self.fields['device'].widget.attrs.update({'id': 'id_device'})