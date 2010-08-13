from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    url = forms.EmailField(label="URL", required=False)
    comment = forms.CharField(label="Comment", widget=forms.Textarea)