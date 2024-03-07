from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path('citizen/', views.citizen_portal, name='citizen-portal'),
    path('agent/', views.agent_portal, name='agent-portal'),
    path('agent/map', views.map, name='map'),
    path('agent/stats', views.stats, name='stats'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('agent-signup/', views.agent_signup, name='agent-signup'),
    path('agent-signin/', views.agent_signin, name='agent-signin'),
	path('report/anonymous/', views.anonymous_report, name='anonymous_report'),
	path('logout/', views.logout_view, name='logout'),
	path('about/', views.about, name='about'),
	path('report/<int:pk>', views.report, name='report'),
	path('view_report/<int:pk>', views.view_report, name='view_report'),
	path('delete/<int:pk>', views.delete_report, name='delete'),
	path('update/<int:pk>', views.update_report, name='update'),
	path('update_status/<int:pk>', views.update_status, name='update_status'),
	path('dashboard-profile/', views.profile, name='profile'),
	path('profile_update/', views.profile_update, name='profile_update'),
]
