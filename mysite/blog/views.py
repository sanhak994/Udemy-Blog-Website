from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                DetailView, CreateView,
                                UpdateView, DeleteView)

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # Grab the post model and filter out based on these conditions
        # use __lte (less than or equal to) to invoke filter                 the - means descending
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

# The mixin will prevent just anyone from making a post
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        # If it is a draft it shouldn't have a publication date
        # So, pub date should be null
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


##########################################################################################
##########################################################################################
##########################################################################################
###### For comments

### Using a decorator for a builtin django func

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required #This view is only avaliable when logged in
def add_comment_to_post(request, pk): #linking the primary key for that post
    post = get_object_or_404(Post, pk=pk) #get the object or the error page

    if request.method == 'POST': # I added the upper to avoid issues with case sensitivity
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk) #So, the bool we had set earlier to False is True
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete() # When we delete it we would have also deleted the pk,
    # which is why we save the comment.post.key in a seperate var
    return redirect('post_detail', pk=post_pk)
