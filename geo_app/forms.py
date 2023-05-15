from django import forms
from .models import UploadFile


class UploadDetailsForm(forms.ModelForm):

    """This form is for uploading details file """

    class Meta:
        model = UploadFile
        fields = ['file_type', 'file']