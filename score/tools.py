import score.models


class CourseInfo:
    """ Course Information """
    def __init__(self, course_id):
        self.course = score.models.Course.objects.get(pk=course_id)
        self._hole_count()
        self._par()
        return

    def _hole_count(self):
        self.hole_count = self.course.hole_set.count()
        return

    def _par(self):
        self.par = {}
        for hole in self.course.hole_set.all():
            self.par[hole.number] = hole.par
        return


class CompetitionInfo:

    def __init__(self, comp_id):
        self.comp = score.models.Competition.objects.get(pk=comp_id)
        self._players()
        return

    def _players(self):
        self.players = self.comp.throw_set.values('player__name').distinct()
        return
