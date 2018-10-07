from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Participant
from .forms import MatchParticipantsForm, CheckMatchForm


def _make_pairs_recursive(matched_participants, pairs=[]):
    if not len(matched_participants):
        return pairs
    starting_participant = matched_participants.pop()
    for participant in matched_participants:
        if participant.match_id == starting_participant.id:
            matched_participants.remove(participant)
            pairs.append((starting_participant, participant))
            return _make_pairs_recursive(matched_participants, pairs)
    return pairs

def make_pairs(matched_participants):
    return _make_pairs_recursive(matched_participants, [])

def index(request):
    participants = Participant.objects.filter(match_id__isnull=True)
    matched_participants = list(Participant.objects.filter(match_id__isnull=False))
    pairs = make_pairs(matched_participants)
    print("PAIRS", pairs)
    template = loader.get_template('index.html')
    context = {
        'participants_one': participants,
        'participants_two': participants,
        'pairs': pairs,
    }
    return HttpResponse(template.render(context, request))


def matchups(request):
    matched_participants = list(Participant.objects.filter(match_id__isnull=False))
    pairs = make_pairs(matched_participants)

    if request.method == 'POST':
        form = MatchParticipantsForm(request.POST)
        if form.is_valid():
            first_participant = form.cleaned_data['first_participant']
            second_participant = form.cleaned_data['second_participant']
            first_participant.match_id = second_participant.id
            first_participant.save()
            second_participant.match_id = first_participant.id
            second_participant.save()
            return HttpResponseRedirect('/matchups/matchups')

    else:
        form = MatchParticipantsForm()

    return render(request, 'matchups.html', {'form': form, 'pairs': pairs})


def remove_pairs(request):
    matched_participants = list(Participant.objects.filter(match_id__isnull=False))
    matched_participants_keep = matched_participants.copy()
    pairs = make_pairs(matched_participants)
    if request.method == 'POST':
        if request.POST['match_id']:
            match_id = int(request.POST['match_id'])
            for participant in matched_participants_keep:
                if participant.match_id == match_id:
                    participant.match_id = None
                    participant.save()
                if participant.id == match_id:
                    participant.match_id = None
                    participant.save()
        return HttpResponseRedirect('/matchups/remove_matchups')
    return render(request, 'remove_pairs.html', {'pairs': pairs})


def check_match(request):
    if request.method == 'POST':
        form = CheckMatchForm(request.POST)
        if form.is_valid():
            first_participant = form.cleaned_data['first_participant']
            second_participant = form.cleaned_data['second_participant']
            first_participant.queries += 1
            second_participant.queries += 1
            first_participant.save()
            second_participant.save()
            if first_participant.match_id == second_participant.id:
                return render(request, 'perfect_match.html', {'first': first_participant,
                                                              'second': second_participant})
            else:
                return render(request, 'no_match.html', {'first': first_participant,
                                                         'second': second_participant})
    else:
        form = CheckMatchForm()
    return render(request, 'check_matchup.html', {'form': form})