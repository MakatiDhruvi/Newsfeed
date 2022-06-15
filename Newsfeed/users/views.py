from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import user_registeration_form, user_update_form, profile_update_form
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = user_registeration_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account has been created and you are able to login as {username}!')
            return redirect('login')

    else:
        form = user_registeration_form()
        return render(request, 'users/register.html', {'form': form})

  
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = user_update_form(request.POST, instance=request.user)
        p_form = profile_update_form(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated..!')
            return redirect('profile')
    else:
        u_form = user_update_form(instance=request.user)
        p_form = profile_update_form(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
