from django.shortcuts import render, get_object_or_404,reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Recipe, Comment
from .forms import CommentForm, EditCommentForm


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class AllRecipes(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'all-recipes.html'
    paginate_by = 6


class FullRecipe(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.recipe_comment.filter(approved=True).order_by('created_on')
        edit_comment_id = request.GET.get('edit_comment_id', '')
        editing_comment = False
        if edit_comment_id:
            edit_comment = get_object_or_404(Comment, pk=edit_comment_id)
            edit_comment_form = EditCommentForm(instance=edit_comment)

            if edit_comment_form.is_valid():
                edit_comment_form.instance.author = request.user
                edit_comment_form.instance.email = request.user.email
                edit_comment_form.instance.name = request.user.username
                comment = edit_comment_form.save(commit=False)
                comment.recipe = recipe
                comment.save()
            else:
                comment_form = CommentForm()
        else:
            edit_comment = None
            edit_comment_form = EditCommentForm()

        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "full-recipe.html",
            {
                "recipe": recipe,
                "edit_comment": edit_comment,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "edit_comment_form": edit_comment_form,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.recipe_comment.filter(approved=True).order_by('created_on')
        editing_comment = False
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        action = request.POST['action']
        if action == 'add_comment':
            comment_form = CommentForm(data=request.POST)
            commented = True

            if comment_form.is_valid():
                comment_form.instance.author = request.user
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.save()
            else:
                comment_form = CommentForm()

            edit_comment_form = EditCommentForm()
            
            return render(
                request,
                "full-recipe.html",
                {
                    "recipe": recipe,
                    "comments": comments,
                    "commented": commented,
                    "liked": liked,
                    "edit_comment_form": edit_comment_form,
                    "comment_form": CommentForm()
                },
            )

        if action == 'edit_comment':
            edit_comment_id = request.GET.get('edit_comment_id', '')
            editing_comment = True
            commented = False
            if edit_comment_id:
                edit_comment = get_object_or_404(Comment, pk=edit_comment_id)

            edit_comment_form = EditCommentForm(request.POST, request.FILES, instance=edit_comment)

            if edit_comment_form.is_valid():
                edit_comment.save()
            else:
                edit_comment_form = EditCommentForm()

            return render(
                request,
                "full-recipe.html",
                {
                    "recipe": recipe,
                    "edit_comment": edit_comment,
                    "comments": comments,
                    "commented": False,
                    "liked": liked,
                    "edit_comment_form": edit_comment_form,
                    "comment_form": CommentForm()
                },
            )

        if action == 'delete_comment':
            delete_comment_id = request.POST['delete_comment_id']
            if delete_comment_id:
                delete_comment = get_object_or_404(Comment, pk=delete_comment_id)
                delete_comment.delete()

        return HttpResponseRedirect(reverse('full-recipe', args=[slug]))


class RecipeLike(View):
    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('full-recipe', args=[slug]))
