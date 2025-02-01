from django.shortcuts import render
from .forms import CostForm


# Create your views here.
def enter_cost(request):
    form = CostForm()
    if request.method == 'POST':
        # CL: ++
        print('')
        print(request.POST)
        print('')
        # CL: --
        form = CostForm(request.POST)
        if form.is_valid():
            c_date = form.cleaned_data['date']
            c_costcategory = form.cleaned_data['costcategory']
            # CL: ++
            print(f"c_date: {c_date}")
            print(f"c_costcategory: {c_costcategory}")
            print('')
            # CL: --
        else:
            print('form is NOT valid!')
            return render(request, 'cost.html', {'form': form})

    context = {'form': form}
    return render(request, 'cost.html', context)
