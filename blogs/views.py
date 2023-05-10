import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from blogs.models import Blog, Blogger, Comment


def index(request):
    """View function for home page of site."""

    num_blogs = Blog.objects.all().count()
    num_bloggers = Blogger.objects.count()

    context = {
        'num_blogs': num_blogs,
        'num_bloggers': num_bloggers,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'blogs/index.html', context=context)


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 1

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class BloggerListView(generic.ListView):
    model = Blogger


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerDetailView(generic.DetailView):
    model = Blogger


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.user = self.request.user
        form.instance.post_date = datetime.date.today()
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })


class BlogCreate(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description', ]
    permission_required = 'blogs.is_blogger'

    def form_valid(self, form):
        form.instance.blogger = self.request.user.blogger
        form.instance.post_date = datetime.date.today()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs', )
