from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class Hole(models.Model):
    course = models.ForeignKey('score.Course',
                               on_delete=models.CASCADE)
    number = models.IntegerField()
    par = models.IntegerField()

    def __str__(self):
        return "{0} hole {1}".format(self.course, self.number)

class Competition(models.Model):
    date = models.DateField()
    game_number = models.IntegerField()
    notes = models.TextField(null=False, blank=True)
    course = models.ForeignKey('score.Course',
                               on_delete=models.PROTECT)

    def get_absolute_url(self):
        return "/match_results_single/{0}/".format(self.id)

    def __str__(self):
        return "{0} on {1} # {2}".format(self.course,
                                         self.date,
                                         self.game_number)

class Throw(models.Model):
    player = models.ForeignKey('score.Player',
                               on_delete=models.PROTECT)
    competition = models.ForeignKey('score.Competition',
                                    on_delete=models.PROTECT)
    hole = models.ForeignKey('score.Hole',
                             on_delete=models.PROTECT)
    throws = models.IntegerField()

    def __str__(self):
        return "{0} {1} {2}".format(self.competition,
                                    self.player,
                                    self.hole)




