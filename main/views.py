from django.shortcuts import render, redirect
from django.db.models import Q
# It will redirect us to the page that we pass in.
from django.urls import reverse_lazy
# HTTP response redirect:
from django.http import HttpResponseRedirect
# Make sure the user is logged in.
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View       # generic view class
from .models import Comment, Post, UserProfile, Notification            # post model
from .forms import PostForm, CommentForm  # from we created
# to update or delete the comment.
from django.views.generic.edit import UpdateView, DeleteView

# Viewing the Listings of the post in the social field:


class PostListView(LoginRequiredMixin, View):
    # through 'get' we're requesting the contents.
    def get(self, request, *args, **kwargs):

        # this will show the posts of the user you're currently following, in newest to oldest order.
        logged_in_user = request.user
        # Using 'Q' object with '&'(AND- operator) or '|'(OR- operator) for chaining the filters.
        posts = Post.objects.filter(
            Q(author__profile__in=[logged_in_user.id]) |
            Q(author__profile__followers__in=[logged_in_user.id])
        ).order_by('-created_on')
        form = PostForm()

        # just a dictionary:
        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'main/post_list.html', context)

    # posting something using 'post' method:
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'main/post_list.html', context)


# View for Comment form:
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'main/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            # To save the form in database.
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'main/post_detail.html', context)

# Gereric View---View for Reply a comment i.e. to reply on a parent comment:


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('post-detail', pk=post_pk)


# Gereric View---View for update a comment i.e. to edit a comment:

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'main/post_edit.html'

    # For redirecting to the detail page of the post we already on:

    def get_success_url(self):
        # to get the primary-key that we have passed in the view.
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    # Function for 'UserPassesTestMixin' test wheather the user is logged in or not:
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Generic View---View to delete a comment:


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'main/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'main/comment_delete.html'

    def get_success_url(self):
        # to get the primary-key that we have passed in the view.
        # This name i.e. 'post_pk' must be same as it is in the urls.py
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        # for followers, using all-method:
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        # for number of followers, using length method:
        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }

        return render(request, 'main/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture', 'cover']
    template_name = 'main/profile_edit.html'

    # For reversing the profile to the actual default profile:
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        # As we've added a 'ManyManyField' in the models.py file; we can add or remove something from many many field in Django.
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        # As we've added a 'ManyManyField' in the models.py file; we can add or remove something from many many field in Django.
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)

# For adding likes to the post:


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'main/search.html', context)


class ListOfFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'main/followers_list.html', context)
