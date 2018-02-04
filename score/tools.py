import score.models


class CourseInfo:
    """ Course Information """
    def __init__(self, course_id):
        self.course = score.models.Course.objects.get(pk=course_id)
        self.hole_count = self.course.hole_set.count()
        self.par = self._par()
        return

    def _par(self):
        par = {}
        for hole in self.course.hole_set.all():
            par[hole.number] = hole.par
        return par


class CompetitionInfo:
    """ Competition Information """
    def __init__(self, comp_id):
        self.comp_object = score.models.Competition.objects.get(pk=comp_id)
        self.throws = self._throws()
        print(self.throws)
        return

    def _throws(self):
        player_throws = {}
        throws = score.models.Throw.objects.filter(competition=self.comp_object)
        for throw in throws:
            player = throw.player.name
            if not player in player_throws:
                player_throws[player] = {}
            player_throws[player][throw.hole.number] = throw.throws
        return player_throws
