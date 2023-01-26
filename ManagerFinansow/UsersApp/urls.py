"""ManagerFinansow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('logout', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('register', views.registerUser, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profiles', views.allProfiles, name='profiles'),
    path('profile', views.profile, name='profile'),
    path('profile/change-password', views.changePassword, name='change-password'),
    path('profile/edit', views.editProfile, name='edit-profile'),
    path('profile/categories', views.showCategories, name='all-categories'),
    path('profile/categories/create', views.createCategory, name='create-category'),
    path('profile/categories/edit/<uuid:pk>', views.editCategory, name='edit-category'),
    path('profile/categories/delete/<uuid:pk>', views.deleteCategory, name='delete-category'),
    path('profile/categories/subcategories/<uuid:pk>', views.allSubcategories, name='all-subcategories'),
    path('profile/categories/subcategories/<uuid:pk>/create-subcategory', 
    views.createSubcategory, name='create-subcategory'),
    path('profile/categories/subcategories/<uuid:pk>/edit-subcategory/<uuid:pk2>', 
    views.editSubcategory, name='edit-subcategory'),
    path('profile/categories/subcategories/<uuid:pk>/delete-subcategory/<uuid:pk2>', 
    views.deleteSubcategory, name='delete-subcategory')
]
