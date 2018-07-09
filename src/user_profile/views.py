from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Il tuo profilo e\' stato correttamente aggiornato')
            #return redirect('/')
            return render(request, 'user_profile/user_profile.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
        else:
            messages.error(request, 'Profilo non aggiornato. Per favore correggi gli errori sottostanti')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_profile/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
