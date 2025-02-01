from django.shortcuts import render
from .forms import FishbuyForm


# Create your views here.
def enter_fishbuy(request):
    form = FishbuyForm()
    if request.method == 'POST':
        # CL: ++
        print(request.POST)
        # CL: --
        form = FishbuyForm(request.POST)
    context = {'form': form}
    return render(request, 'fishbuy.html', context)
