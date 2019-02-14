from django.contrib import admin
from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [
    path('logout/', views.logout_view, name = 'logout'),
    path('setter/', views.setter_view, name = 'setter'),
    path('challenge/<slug:slug>', views.challenge_view, name = 'challenge'),
    path('challenge/<slug:challenge_slug>/newquestion', views.new_question_view, name = 'new_question'),
    path('question/<slug:question_slug>', views.question_view, name = 'question'),
    path('challenge/<slug:challenge_slug>/newcollaborator', views.collaborator_view, name = 'collaborator'),
    path('challenge/<slug:challenge_slug>/removecollaborator/<str:collaborator>', views.remove_collaborator_view, name = 'remove_collaborator'),
    path('challenge/<slug:challenge_slug>/leaderboard', views.leaderboard_view, name = 'leaderboard'),
    path('challenge/<slug:challenge_slug>/report', views.report_view, name = 'report'),
    path('challenge/<slug:challenge_slug>/remove', views.remove_challenge_view, name = 'remove_challenge'),
    path('question/<slug:question_slug>/remove', views.remove_question_view, name = 'remove_question'),
    path('question/<slug:question_slug>/editorial', views.editorial_view, name = 'editorial'),
    path('random_question', views.random_question_view, name = 'random_question'),
    path('manage/remove_setter/<slug:setter_name>', views.remove_setter_view, name = 'remove_setter'),
    #parag
    path('profile/', views.redirecter_view, name = 'user_profile'),
    path('profile/<slug:profile_slug>/', views.account_view, name = 'profile'),
    path('profile/<slug:profile_slug>/edit/', views.edit_view, name = 'profile_edit'),
    path('profile/<slug:profile_slug>/changepass/', views.change_password, name = 'change_password'),
    path('profile/<slug:profile_slug>/deletepic/', views.delete_pic, name = 'profile_delete_pic'),
    path('contests/', views.contest_view, name = 'contests'),
    #pravin
    path('practice/', views.practice_view, name = 'practice'),
    #mradul
    path('manage/', views.admin_view, name = 'admin_mcqts'),
]
