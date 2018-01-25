from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import score.models
from score.tools import CourseInfo, CompetitionInfo
from score.forms import CourseAdd

@login_required
def competition_results_list(request, id=None):
    matches = score.models.Competition.objects.all()
    return render(request, 'score_competition_list_table.html', {'username':request.user,
                                               'match_id': id,
                                               'matches': matches})


@login_required
def competition_results_single(request, id=None):
    match_throws =  {}
    if id:
        match_meta = score.models.Competition.objects.get(pk=id)
        course_meta = CourseInfo(match_meta.course_id)
        throw_data = match_meta.throw_set

        comp_data = CompetitionInfo(id)
    return render(request, 'score_competition_r.html.html', {'match_meta': match_meta,
                                                         'course_meta': course_meta,
                                                         'comp_data': comp_data,
                                                         'username': request.user,})


def course_add(request):
    form = CourseAdd(request.POST or None)
    if form.is_valid():
        pass
        return redirect("course_created")
    return render(request, "score_course_cu.html", {'form': form})

def competition_add():
    pass