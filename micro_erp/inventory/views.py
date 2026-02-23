from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, View
from micro_erp.inventory.models import StockMovement, StockLevel

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
    
class StockLevelJsonView(View):
    def get(self, request, *args, **kwargs):
        location_id = self.kwargs['location_id']
        stock_level = StockLevel.objects.filter(location_id=location_id)

        data = {
            'labels': [stock_level.product.name for stock_level in stock_level],
            'data': [stock_level.quantity for stock_level in stock_level]
        }

        return JsonResponse(data, safe=False)