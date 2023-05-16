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
    # Define the GET request
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.recipe_comment.filter(approved=True).order_by('-created_on')
        edit_comment_id = request.GET.get('edit_comment_id', '')
        editing_comment = False
        # If the user is editing a comment
        if edit_comment_id:
            edit_comment = get_object_or_404(Comment, pk=edit_comment_id)
            edit_comment_form = EditCommentForm(instance=edit_comment)
            # Save the edited comment
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

        # Set Liked to true if the user has "Liked" this recipe
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Return the context elements to be rendered
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

    # Define the POST request
    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.recipe_comment.filter(approved=True).order_by('-created_on')
        editing_comment = False

        # Set Liked to true if the user has "Liked" this recipe
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Get the Action that the user is performing from the hidden field on the Add / Edit / Delete form and buttons
        action = request.POST['action']
        # If the user is Adding a comment
        if action == 'add_comment':
            comment_form = CommentForm(data=request.POST)
            commented = True
            # Validate the form and save the comment if valid
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

            # Return the context elements to be rendered
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

        # If the user is Editing a comment
        if action == 'edit_comment':
            edit_comment_id = request.GET.get('edit_comment_id', '')
            editing_comment = True
            commented = False
            # Get the Comment to be Edited
            if edit_comment_id:
                edit_comment = get_object_or_404(Comment, pk=edit_comment_id)

            # Set up the EditContentForm with the Comment being Edited
            edit_comment_form = EditCommentForm(request.POST, request.FILES, instance=edit_comment)

            # If the form is valid, save the Comment
            if edit_comment_form.is_valid():
                edit_comment.save()
            else:
                edit_comment_form = EditCommentForm()

            # Return the context elements to be rendered
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

        # If the user is Deleting a comment
        if action == 'delete_comment':
            # Get the Comment ID of the Comment to be Deleted
            delete_comment_id = request.POST['delete_comment_id']
            if delete_comment_id:
                # Get the Comment to be Deleted
                delete_comment = get_object_or_404(Comment, pk=delete_comment_id)
                # Delete the Comment
                delete_comment.delete()

        # Return the user to the Recipe
        return HttpResponseRedirect(reverse('full-recipe', args=[slug]))


class RecipeLike(View):
    def post(self, request, slug):
        # Get the Recipe that the likes are related to
        recipe = get_object_or_404(Recipe, slug=slug)

        # If the user already likes the recipe
        if recipe.likes.filter(id=request.user.id).exists():
            # Remove the Like
            recipe.likes.remove(request.user)
        else:
            # Add the user's Like
            recipe.likes.add(request.user)

        # Return the user to the Recipe
        return HttpResponseRedirect(reverse('full-recipe', args=[slug]))
