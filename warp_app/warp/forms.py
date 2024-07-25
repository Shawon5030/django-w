from django import forms

class WarpForm(forms.Form):
    warp_client_id = forms.CharField(label='WARP ID', max_length=100)
    gb_to_add = forms.IntegerField(label='  GB Add ', min_value=1)