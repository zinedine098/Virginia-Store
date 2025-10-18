from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware untuk memaksa login di semua halaman.
    Halaman yang dikecualikan:
    - login
    - logout
    - admin
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Jika user sudah login, biarkan
        if not request.user.is_authenticated:
            login_url = reverse('login')

            # URL yang dikecualikan
            allowed_urls = [
                login_url,
                reverse('logout'),
                '/admin/',  # admin bisa diakses tanpa login middleware (atau sesuaikan)
            ]

            # Jangan redirect untuk allowed_urls
            if not any(request.path.startswith(url) for url in allowed_urls):
                return redirect(login_url)

        response = self.get_response(request)
        return response
