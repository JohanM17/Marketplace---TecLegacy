from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from cart.models import Cart


class UserLoginView(LoginView):
    """Vista de login personalizada para manejar la opción 'Recordarme'."""
    template_name = 'users/login.html'

    def form_valid(self, form):
        # Si el checkbox 'remember' no está marcado, la sesión expira al cerrar el navegador
        remember_me = self.request.POST.get('remember')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        else:
            # Si está marcado, la sesión dura 2 semanas (valor por defecto de Django)
            self.request.session.set_expiry(None)
        return super().form_valid(form)


def register(request):
    """Vista para registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Vista para ver y actualizar el perfil del usuario."""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def order_history(request):
    """Vista para mostrar el historial de pedidos del usuario."""
    orders = request.user.order_set.all().order_by('-created_at')
    return render(request, 'users/order_history.html', {'orders': orders})

def logout_view(request):
    # Vaciar el carrito de la cuenta antes de cerrar sesión
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('products:index')