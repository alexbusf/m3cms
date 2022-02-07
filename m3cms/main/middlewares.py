from .models import Category


def m3cms_context_processor(request):
    context = {'categories': Category.objects.all()}
    return context
