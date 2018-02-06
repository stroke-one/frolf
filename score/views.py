from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import score.models
from score.tools import CourseInfo, CompetitionInfo
from score.forms import CourseAdd, CourseUpdate, CompCreate, CompUpdate


@login_required
def competition_results_list(request, match_id=None):
    matches = score.models.Competition.objects.all()
    return render(request, 'score_competition_list_table.html', {'username': request.user,
                                                                 'match_id': match_id,
                                                                 'matches': matches})


@login_required
def competition_results_single(request, match_id=None):
    if match_id:
        match_meta = score.models.Competition.objects.get(pk=match_id)
        course_meta = CourseInfo(match_meta.course_id)
        comp_data = CompetitionInfo(match_id)
    return render(request, 'score_competition_r.html', {'match_meta': match_meta,
                                                        'course_meta': course_meta,
                                                        'comp_data': comp_data,
                                                        'username': request.user, })


def course_create(request):
    form = CourseAdd(request.POST or None)
    if form.is_valid():
        record = score.models.Course()
        record.name = form.cleaned_data['course_name']
        record.save()
        for n in range(1, form.cleaned_data['hole_count'] + 1):
            h = score.models.Hole()
            h.course = record
            h.number = n
            h.par = 0
            h.save()
        return HttpResponseRedirect("course_created/{0}".format(record.id))

    return render(request, "score_course_c.html", {'form': form})


def course_update(request, course_id=None):
    try:
        hole_count = len(score.models.Hole.objects.filter(course=course_id))
    except:
        return Http404("Error retrieving record")

    form = CourseUpdate(request.POST or None, hole_count=hole_count, course_id=course_id)
    if form.is_valid():
        # TODO WHY IS THIS SWITCHING FROM THE KWARG TO A FUNCTION?
        course_id = form.get_course_id()
        holes = score.models.Hole.objects.filter(course=course_id)
        hole_par_dict = form.hole_par()
        for hole in holes:
            if hole.number in hole_par_dict:
                hole.par = hole_par_dict[hole.number]
                hole.save()
        return HttpResponseRedirect("/course_read/{0}".format(course_id))

    return render(request, "score_course_u.html", {'form': form})


def course_read(request, course_id=None):
    try:
        course_obj = score.models.Course.objects.filter(pk=course_id)
    except:
        return Http404("Could not locate that course")

    holes = score.models.Hole.objects.filter(course=course_id)
    return render(request, "score_course_r.html", {'course': course_obj,
                                                   'holes': holes})


def competition_create(request):
    form = CompCreate(request.POST or None)
    if form.is_valid():
        course = form.cleaned_data['course_select']
        date = form.cleaned_data['match_date']
        game = form.cleaned_data['match_number']
        notes = form.cleaned_data['notes']
        comp = score.models.Competition()
        comp.course_id = course
        comp.date = date
        comp.notes = notes
        comp.game_number = game
        comp.save()
        player_count = form.cleaned_data['player_count']
        return HttpResponseRedirect(
            "/match_results_add/{0}/{1}/{2}".format(course, player_count, comp.id))
    return render(request, 'score_competition_c.html', {'form': form})


def competition_update(request, course_id=None, players=None, comp_id=None):
    course_meta = CourseInfo(course_id)
    form = CompUpdate(request.POST or None, course_id=course_id,
                      player_count=players, course_meta=course_meta,
                      comp_id=comp_id)
    if form.is_valid():
        player_scores = form.get_player_scores()
        player_ids = form.get_player_ids()
        comp_id = form.comp_id

        all_holes = {}
        all_holes_queryset = score.models.Hole.objects.filter(course_id=form.course_id).values('number', 'id')
        for hole in all_holes_queryset:
            all_holes[hole['number']] = hole['id']
        print(all_holes)
        for player_id in player_ids:
            player = player_ids[player_id]
            throws_round = player_scores[player_id]
            for hole in throws_round:
                throw = score.models.Throw()
                throw.competition_id = comp_id
                throw.player_id = player
                throw.hole_id = all_holes[hole]
                throw.throws = throws_round[hole]
                throw.save()
        return HttpResponseRedirect("/match_results_single/{0}".format(comp_id))
    return render(request, 'score_competition_u.html', {'form': form})
