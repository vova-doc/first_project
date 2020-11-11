from django.views.generic import TemplateView, ListView

from applications.blog.models import Post


class IndexView(ListView):
    template_name = "blog/index.html"
    queryset = Post.objects.filter(visible=True)


    # model = Post - то, что делает функция ниже
    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     ctx["object_list"] = Post.objects.all
    #     return ctx
    


