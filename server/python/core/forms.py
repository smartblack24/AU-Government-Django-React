from codemirror import CodeMirrorTextarea
from core.models import PDF
from django import forms

codemirror_widget = CodeMirrorTextarea(
    mode="xml",
    custom_css=("codemirror/custom.css",)
)


class PdfForm(forms.ModelForm):
    html = forms.CharField(widget=codemirror_widget)

    class Meta:
        model = PDF
        fields = "__all__"
