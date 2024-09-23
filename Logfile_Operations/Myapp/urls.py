from django.urls import path
from . import views

urlpatterns=[
    path('',views.User_Login,name='User_Login'),
    path('Register',views.Register,name='Register'),
    path('Dashboard/<str:user_name>',views.Dashboard,name='Dashboard'),
    path('Get_Strings_Logs/<str:user_name>',views.Get_Strings_Logs,name='Get_Strings_Logs'),
    path('Visualization_Task/<str:user_name>',views.Visualization_Task,name='Visualization_Task'),
    # path('Visualization/<str:user_name>',views.Visualization,name='Visualization'),
    # path('Searching_CSV/<str:user_name>',views.Searching_CSV,name='Searching_CSV'),
    # path('search_words/<str:user_name>',views.search_words,name='search_words'),
    path('User_Forgot_Password',views.User_Forgot_Password,name='User_Forgot_Password'),
    path('User_Verfiy_Otp',views.User_Verfiy_Otp,name='User_Verfiy_Otp'),
    path('User_Logout',views.User_Logout,name='User_Logout'),
    path('Resend_Otp',views.Resend_Otp,name='Resend_Otp'),
    # path('Read_Logfile',views.Read_Logfile,name='Read_Logfile'),
    # path('chart_view',views.chart_view,name='chart_view'),
    path('Soring_Word_Wise',views.Soring_Word_Wise,name='Soring_Word_Wise'),
    path('Sorting_Data/<str:user_name>',views.Sorting_Data,name='Sorting_Data'),
    path('Healthy/<str:user_name>',views.Healthy,name="Healthy")
    
]