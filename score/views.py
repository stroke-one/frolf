from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import score.models
from score.tools import CourseInfo, CompetitionInfo
from score.forms import CourseAdd, CourseUpdate

@login_required
def competition_results_list(request, id=None):
    matches = score.models.Competition.objects.all()
    return render(request, 'score_competition_list_table.html', {'username':request.user,
                                               'match_id': id,
                                               'matches': matches})


@login_required
def competition_results_single(request, id=None):
    if id:
        match_meta = score.models.Competition.objects.get(pk=id)
        course_meta = CourseInfo(match_meta.course_id)
        comp_data = CompetitionInfo(id)
    return render(request, 'score_competition_r.html', {'match_meta': match_meta,
                                                         'course_meta': course_meta,
                                                         'comp_data': comp_data,
                                                         'username': request.user,})


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

def course_update(request, id=None):
    try:
        hole_count = len(score.models.Hole.objects.filter(course=id))
    except:
        return Http404("Error retrieving record")

    form = CourseUpdate(request.POST or None, hole_count=hole_count, course_id=id)
    if form.is_valid():
        course_id = form.get_course_id()
        holes = score.models.Hole.objects.filter(course=course_id)
        hole_par_dict = form.hole_par()
        for hole in holes:
            if hole.number in hole_par_dict:
                hole.par = hole_par_dict[hole.number]
                hole.save()
        return HttpResponseRedirect("/course_read/{0}".format(course_id))

    return render(request, "score_course_u.html", {'form': form})

def course_read(request, id=None):
    try:
        course_obj = score.models.Course.objects.filter(pk=id)
    except:
        return Http404("Could not locate that course")

    holes = score.models.Hole.objects.filter(course=id)
    return render(request, "score_course_r.html", {'course': course_obj,
                                                   'holes': holes})



def competition_add():
    pass