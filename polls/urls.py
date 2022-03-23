from django.urls import path
from . import views

app_name='polls'
urlpatterns=[
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail' ),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create_question', views.CreateQuestion.as_view(), name='new_question'),
    path('update_question/<int:pk>/', views.QuestionUpdate.as_view(), name='modify_question'),
    path('delete/<int:pk>/', views.QuestionDelete.as_view(), name='delete_question'),
    path('create_choice/<str:question_text>/', views.CreateChoice.as_view(), name='new_choice'),
    path('update_choice/<int:pk>/', views.ChoiceUpdate.as_view(), name='modify_choice'),
    path('delete/<int:pk>/', views.ChoiceDelete.as_view(), name='delete_choice'),
]