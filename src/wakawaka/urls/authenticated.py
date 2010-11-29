from django.contrib.auth.decorators import login_required
from wakawaka.urls import decorated_urlpatterns


urlpatterns = decorated_urlpatterns(login_required)
