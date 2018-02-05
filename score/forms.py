from django import forms
import score.models

class CourseAdd(forms.Form):
    course_name = forms.CharField(label="Course Name", max_length="100")
    hole_count = forms.IntegerField(label="Number of Holes")


class CourseUpdate(forms.Form):

    def __init__(self, *args, **kwargs):
        hole_count = kwargs.pop('hole_count')
        self.course_id = kwargs.pop('course_id')
        super(CourseUpdate, self).__init__(*args, **kwargs)

        for n in range(1, hole_count + 1):
            print(n)
            self.fields["hole_{0}".format(n)] = forms.IntegerField(label=str(n).zfill(2))

    def hole_par(self):
        hole_par_dict = {}
        for name, par in self.cleaned_data.items():
            if name.startswith("hole_"):
                hole_number = self.fields[name].label
                hole_number = int(hole_number.replace("hole_", ""))
                hole_par_dict[hole_number] = par
        return hole_par_dict

    def get_course_id(self):
        return self.course_id

class CompCreate(forms.Form):
    course_select = forms.ChoiceField(label="Select Course")
    match_date = forms.DateField(label="Date of Match")
    match_number = forms.IntegerField(label="Round (if multiple)")
    player_count = forms.IntegerField(label="Player Count")
    notes = forms.CharField(label="Notes", widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(CompCreate, self).__init__(*args, **kwargs)
        courses = []
        course_query = score.models.Course.objects.all()
        for c in course_query:
            courses.append((c.id, c.name))
        self.fields['course_select'].choices = courses


class CompUpdate(forms.Form):
    def get_player_ids(self):
        """
        Retrieve player number assigned by form to the actual
        player.id from the score model
        :return: dict {player_number: player.id}
        """
        player_id = {}
        for data_field, val in self.cleaned_data.items():
            if data_field.startswith("player_"):
                player_number = int(data_field.replace("player_", ""))
                if not player_number in player_id:
                    player_id[player_number] = {}
                    player_id[player_number] = int(val)
        return player_id

    def get_player_scores(self):
        """
        Retrieve player number assigned by form to dict containing scores
        :return: dict {player_number: {hole_number, score}}
        """
        player_score = {}
        for data_field, val in self.cleaned_data.items():
            if data_field.startswith("p_"):
                # because the form fields are created dynamically depending
                # on the length of the course the workaround is to name
                # them for the throwing player, and the number of the hole.
                # split the field to pull out player_num and hole_num
                p_id_h_id = data_field.split("_")
                p_id = int(p_id_h_id[1])
                h_id = int(p_id_h_id[3])

                if not p_id in player_score:
                    player_score[p_id] = {}
                player_score[p_id][h_id] = int(val)
        return player_score

    def __init__(self, *args, **kwargs):
        player_count = int(kwargs.pop('player_count'))
        self.course_id = int(kwargs.pop('course_id'))
        self.comp_id = int(kwargs.pop('comp_id'))
        self.course_meta = kwargs.pop('course_meta')
        super(CompUpdate, self).__init__(*args, **kwargs)

        player_choice_list = []
        all_players = score.models.Player.objects.all()
        for player in all_players:
            player_choice_list.append((player.id, player.name))

        hole_objects = score.models.Hole.objects.filter(course=self.course_id)
        course_length = len(hole_objects)

        for p in range(player_count):
            self.fields['player_{0}'.format(str(p).zfill(2))] = forms.ChoiceField(label="Select Player",
                                                                                  choices=player_choice_list)
            for c in range(1, course_length + 1):
                # using 1 index on this range to make the cross reference
                # against the hole object more straightforward
                hole_name = 'p_{0}_h_{1}'.format(str(p).zfill(2), str(c).zfill(2))
                self.fields[hole_name] = forms.IntegerField()
                self.fields[hole_name].label = "Hole {0}".format(str(c).zfill(2))





