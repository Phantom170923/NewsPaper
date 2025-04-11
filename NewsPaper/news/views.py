from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.widgets import HiddenInput

from .filters import PostFilter
from .forms import PostForm
from .models import Post, PostCategory, Comment


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_update_post.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_type = kwargs.get('post_type')

        if self.post_type not in ['news', 'article']:
            raise Http404("Неверный тип материала")

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'choice': self.post_type}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['choice'].widget = HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Создание {'новости' if self.post_type == 'news' else 'статьи'}"
        return context


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_update_post.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.post_type = self.object.choice

        if self.post_type not in ['news', 'article']:
            raise Http404("Неверный тип материала")

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'choice': self.post_type}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['choice'].widget = HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование {'новости' if self.post_type == 'news' else 'статьи'}"
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.post_type = self.object.choice

        if self.post_type not in ['news', 'article']:
            raise Http404("Неверный тип материала")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Удаление {'новости' if self.post_type == 'news' else 'статьи'}"
        return context
