"""frolf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
# from django.conf.urls import url, include
from django.urls import path
import core.views
import score.views

urlpatterns = [
    path('', core.views.default, name="index"),
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, {'template_name': 'login.html'}),
    path('logout/', auth_views.logout, {'template_name': 'logout.html'}),
    path('match_results_view', score.views.competition_results_list),
    path('match_results_single/<int:id>/', score.views.competition_results_single),
    path('course_create', score.views.course_create),
    path('course_created/<int:course_id>/', score.views.course_update),
    path('course_read/<int:course_id>/', score.views.course_read),
    path('match_results_create', score.views.competition_create),
    path('match_results_add/<int:course_id>/<int:players>/<int:comp_id>/', score.views.competition_update),
    # path('match_results_add', score.views.default, name="add"),

]
