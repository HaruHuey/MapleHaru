from django import forms
from .models import MapleDB

def validator_MapleName(value):
    if len(value) < 2:
        raise forms.ValidationError('두 글자 이상 입력해주세요')

class MapleNameForm(forms.Form):
    MapleName = forms.CharField(validators=[validator_MapleName], label='', widget=forms.TextInput)

    # pylint Maybe no member 오류 처리
    # pylint: disable=maybe-no-member
    MapleName.widget.attrs.update({
        'class': 'form-control setting-border',
        'placeholder': '메이플 닉네임을 입력해주세요...',
        'aria-label': "메이플 닉네임을 입력해주세요...",
        'aria-describedby': "button-addon2",
    })