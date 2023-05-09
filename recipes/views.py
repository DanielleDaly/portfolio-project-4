from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Recipe
from .forms import CommentForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class FullRecipe(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "full-recipe.html",
            {
                "recipe": recipe,
                "comment_form": CommentForm()
            },
        )
    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "full-recipe.html",
            {
                "recipe": recipe,
                "commented": True,
                "comment_form": CommentForm()
            },
        )
