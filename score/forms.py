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

class CompAdd(forms.Form):
    course_select = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(CompAdd, self).__init__(*args, **kwargs)
        courses = []
        course_query = score.models.Course.objects.all()
        for c in course_query:
            courses.append((c.id, c.name))
        self.fields['course_select'].choices = courses







