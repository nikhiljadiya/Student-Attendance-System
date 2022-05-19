from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from attendance_app import views as v


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', v.index),
    url(r'^dashboard/$', v.dashboard, name="dashboard"),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout, {'next_page': '/login/'}),
    url(r'^manage_stream/$', v.manage_stream, name="manage_stream"),
    url(r'^stream/(?P<action>\w+)/(?P<stream_id>[0-9]+)/$', v.manage_stream, name='stream_action'),
    url(r'^manage_semester/$', v.manage_semester, name="manage_semester"),
    url(r'^semester/(?P<action>\w+)/(?P<semester_id>[0-9]+)/$', v.manage_semester, name='semester_action'),
    url(r'^manage_subject/$', v.manage_subject, name="manage_subject"),
    url(r'^subject/(?P<action>\w+)/(?P<subject_id>[0-9]+)/$', v.manage_subject, name='subject_action'),
    url(r'^ajax_get_semesters/$', v.ajax_get_semesters, name='ajax_get_semesters'),
    url(r'^ajax_get_subjects/$', v.ajax_get_subjects, name='ajax_get_subjects'),
    url(r'^ajax_get_students/$', v.ajax_get_students, name='ajax_get_students'),
    url(r'^manage_student/$', v.manage_student, name="manage_student"),
    url(r'^student/(?P<action>\w+)/(?P<student_id>[0-9]+)/$', v.manage_student, name='student_action'),
    url(r'^manage_attendance/$', v.manage_attendance, name="manage_attendance"),
    url(r'^attendance/(?P<action>\w+)/(?P<attendance_id>[0-9]+)/$', v.manage_attendance, name='attendance_action'),
    url(r'^manage_student_promotion/$', v.manage_student_promotion, name="manage_student_promotion"),
    url(r'^student_attendance_report$', v.student_attendance_report, name="student_attendance_report"),
    url(r'^test/$', v.test, name='test'),
]
