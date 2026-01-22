from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Capture session key before login (which cycles the key)
        old_session_key = self.request.session.session_key
        
        # Log the user in
        response = super().form_valid(form)
        
        # Merge carts
        if old_session_key:
             from services.cart_service import CartService
             CartService.merge_carts_after_login(self.request, old_session_key, self.request.user)
             
        return response

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Optional: Auto-login after registration
        # user = form.save()
        # login(self.request, user)
        # return redirect('home')
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('home')
