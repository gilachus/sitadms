from django.shortcuts import render, redirect


def landing(request):
    if request.user.is_authenticated:
        return redirect('users:inicio')
    return render(request, 'landing.html', {})


# def error_404(request):
#         data = {}
#         return render(request,'error_404.html', data)