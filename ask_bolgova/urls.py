from django.urls import path

from ask_bolgova import views

urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('hot/', views.hot, name="hot"),
    path('tag/<tag>/', views.tag, name="tag"),
    path('ask/', views.ask, name="ask"),
    path('profile/', views.profile, name="profile"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup", kwargs={'redirect_authenticated_user': True}),
]
