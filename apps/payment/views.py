from django.shortcuts import render

# Create your views here.
def payment_callback(request):
    print(request.GET)
    context = {
        "data": request.GET
    }
    return render(request, 'payment/callback.html/', context)
   