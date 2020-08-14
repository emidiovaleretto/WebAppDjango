from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>', views.recipe, name='recipe'),
    path('searching', views.searching, name='searching'),
    path('new/recipe', views.new_recipe, name='new_recipe'),
    path('delete/<int:recipe_id>', views.delete_recipe, name='delete_recipe'),
    path('dashboard', views.dashboard, name='dashboard'),
    path(r'(?P<id>\d+)/favorite_recipe/$', views.favorite_recipe, name='favorite_recipe'),
    path('edit/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('update_recipe', views.update_recipe, name='update_recipe'),
]
