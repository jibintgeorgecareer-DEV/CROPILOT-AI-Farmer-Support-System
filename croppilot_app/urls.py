from django.urls import path
from . import views

urlpatterns = [

    #user verification
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Farmer registration
    path('farmer/register/', views.farmer_register, name='farmer_register'),

    #farmer dash
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),

    path('farmer/disease/', views.disease_detection, name='disease_detection'),
    path('farmers/all_results',views.farmer_all_results,name='all_results'),
    path('farmer/query/', views.send_query, name='send_query'),
    path('farmer/feedback/', views.submit_feedback, name='submit_feedback'),

    # Farmer – view data
    path('farmer/replies/', views.farmer_queries, name='farmer_replies'),
    path('farmer/crops/', views.farmer_crops, name='farmer_crops'),
    path('farmer/market-prices/', views.farmer_market_prices, name='farmer_market_prices'),
    path('farmer/profile/',views.farmer_profile,name='farmer_profile'),
    path('farmer/edit_profile',views.edit_profile,name='edit_profile'),

    # Soil recomendation
    path(
        'farmer/smart-soil/',
        views.smart_soil_recommendation,
        name='smart_soil'
    ),

    path('chatbot_page/',views.chatbot_page, name='chatbot_page'), #Chatbot Page
    path('chat/',views.chatbot,name='chat'), #chatbot


    # =====================================================
    # AGRICULTURE OFFICER MODULE
    # =====================================================
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),

    path(
        'officer/verify-disease/<int:report_id>/',
        views.officer_verify_disease,
        name='officer_verify_disease'
    ),

    path(
        'officer/reply-query/<int:query_id>/',
        views.reply_query,
        name='reply_query'
    ),


    # =====================================================
    # ADMIN MODULE
    # =====================================================
    path('adminpanel/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Officer management
    path('adminpanel/add-officer/', views.add_officer, name='add_officer'),

    path(
        'adminpanel/officer/edit/<int:officer_id>/',
        views.edit_officer,
        name='edit_officer'
    ),

    path(
        'adminpanel/officer/delete/<int:officer_id>/',
        views.delete_officer,
        name='delete_officer'
    ),

    # Admin data management
    path('adminpanel/farmers/', views.manage_farmers, name='manage_farmers'),
    path('adminpanel/officers/', views.manage_officers, name='manage_officers'),
    path('adminpanel/crops/', views.manage_crops, name='manage_crops'),
    path(
        'adminpanel/market-prices/',
        views.manage_market_prices,
        name='manage_market_prices'
    ),

]
