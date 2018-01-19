from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import score.models
from score.tools import CourseInfo, CompetitionInfo

@login_required
def match_results_view(request, id=None):
    matches = score.models.Competition.objects.all()
    return render(request, 'match_view.html', {'username':request.user,
                                               'match_id': id,
                                               'matches': matches})


@login_required
def match_results_single(request, id=None):
    match_throws =  {}
    if id:
        match_meta = score.models.Competition.objects.get(pk=id)
        course_meta = CourseInfo(match_meta.course_id)
        throw_data = match_meta.throw_set

        comp_data = CompetitionInfo(id)



    return render(request, 'match_results_single.html', {'match_meta': match_meta,
                                                         'course_meta': course_meta,
                                                         'comp_data': comp_data,
                                                         'username': request.user,})