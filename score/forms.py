from django import forms

class CourseAdd(forms.Form):
    course_name = forms.CharField(label="Course Name", max_length="100")
    hole_count = forms.IntegerField(label="Number of Holes")

