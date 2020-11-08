from django.urls import path
import user_data.views as views
urlpatterns = [
    path('insert/', views.UserDataEntry.as_view(), name = 'user_data_entry'),
]