from django import forms

from .models import Participant

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class MatchParticipantsForm(forms.Form):
    first_participant = forms.ModelChoiceField(queryset=Participant.objects.filter(match_id__isnull=True))
    second_participant = forms.ModelChoiceField(queryset=Participant.objects.filter(match_id__isnull=True))

    def clean(self):
        cleaned_data = super().clean()
        first_participant = cleaned_data['first_participant']
        second_participant = cleaned_data['second_participant']

        if first_participant == second_participant:
            raise ValidationError(_('Both participants are the same'))


class CheckMatchForm(forms.Form):
    first_participant = forms.ModelChoiceField(queryset=Participant.objects.filter(match_id__isnull=False))
    first_participant_password = forms.CharField(max_length=50)
    second_participant = forms.ModelChoiceField(queryset=Participant.objects.filter(match_id__isnull=False))
    second_participant_password = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        first_participant = cleaned_data['first_participant']
        first_participant_password = cleaned_data['first_participant_password']
        second_participant = cleaned_data['second_participant']
        second_participant_password = cleaned_data['second_participant_password']

        print(first_participant.password, first_participant_password)

        if first_participant == second_participant:
            raise ValidationError(_('Both participants are the same'))

        if first_participant.password != first_participant_password:
            raise ValidationError(_('First Participant password incorrect'))

        if second_participant.password != second_participant_password:
            raise ValidationError(_('Second Participant password incorrect'))

        if first_participant.queries >= first_participant.query_limit:
            raise ValidationError(_('{} has already reached their limit of guesses!').format(
                first_participant.person_one_first_name))

        if second_participant.queries >= second_participant.query_limit:
            raise ValidationError(_('{} has already reached their limit of guesses!').format(
                second_participant.person_one_first_name))