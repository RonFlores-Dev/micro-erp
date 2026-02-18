from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from micro_erp.inventory.models import StockMovement

# Create your views here.

class HTMXRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    

class HomeView(TemplateView):
    template_name = 'inventory/home.html'

class StockMovementListView(HTMXRequiredMixin, ListView):
    model = StockMovement
    context_object_name = 'stock_movements'
    template_name = 'includes/table_body.html'
    paginate_by = 10

    def get_queryset(self):
        return StockMovement.objects.all().order_by('-timestamp')