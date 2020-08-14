from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Recipe


def index(request):
    recipes = Recipe.objects.order_by('-date').filter(published=True)
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    per_page = paginator.get_page(page)

    data = {
        'recipes': per_page
    }

    return render(request, 'index.html', data)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_favorite = False

    if recipe.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    recipe_to_show = {

        'recipe': recipe,
        'is_favorite': is_favorite,
    }

    return render(request, 'recipe.html', recipe_to_show)


def searching(request):
    recipe_list = Recipe.objects.order_by('-date').filter(published=True)

    if 'search' in request.GET:
        name_to_search = request.GET['search']

        if searching:
            recipe_list = recipe_list.filter(name__icontains=name_to_search)

    data = {

        'recipes': recipe_list
    }

    return render(request, 'searching.html', data)


def new_recipe(request):
    if request.method == 'POST':
        name_recipe = request.POST['name_recipe']
        ingredients = request.POST['ingredients']
        directions = request.POST['directions']
        cook_time = request.POST['cook_time']
        servings = request.POST['servings']
        category = request.POST['category']
        image = request.FILES['image']

        user = get_object_or_404(User, pk=request.user.id)
        recipe = Recipe.objects.create(person=user, name=name_recipe,
                                       ingredients=ingredients, directions=directions, time_to_cook=cook_time,
                                       servings=servings, category=category, image=image)
        recipe.save()
        return redirect('index')
    else:
        return render(request, 'users/new_recipe.html')


def favorite_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.favorite.filter(id=request.user.id).exists():
        recipe.favorite.remove(request.user.id)
    else:
        recipe.favorite.add(request.user.id)
    return redirect('dashboard')


def dashboard(request):
    if request.user.is_authenticated:
        is_favorite = request.user.id
        recipe = Recipe.objects.order_by('-date').filter(favorite=is_favorite)
        paginator = Paginator(recipe, 6)
        page = request.GET.get('page')
        per_page = paginator.get_page(page)

        data = {

            'recipes': per_page,
        }

        return render(request, 'users/dashboard.html', data)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('index')


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_to_edit = {
        'recipe': recipe
    }
    return render(request, 'users/edit_recipe.html', recipe_to_edit)


def update_recipe(request):
    if request.method == 'POST':
        receita_id = request.POST['recipe_id']
        recipe = Recipe.objects.get(pk=receita_id)
        recipe.name = request.POST['name_recipe']
        recipe.ingredients = request.POST['ingredients']
        recipe.directions = request.POST['directions']
        recipe.time_to_cook = request.POST['cook_time']
        recipe.servings = request.POST['servings']
        recipe.category = request.POST['category']
        if 'image' in request.FILES:
            recipe.image = request.FILES['image']
        recipe.save()
        return redirect('index')
