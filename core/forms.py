from django import forms

class UserImportForm(forms.Form):
    excel_file = forms.FileField(label="เลือกไฟล์ Excel (.xlsx)")