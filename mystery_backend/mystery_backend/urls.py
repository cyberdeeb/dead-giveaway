"""
URL configuration for mystery_backend project.

"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from game.views import CaseCreateAPIView, CaseDetailAPIView, GuessAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return HttpResponse("""
    <html>
    <head><title>Dead Giveaway Mystery API</title></head>
    <body>
        <h1>Dead Giveaway - Mystery Game API</h1>
        <p>Welcome to the Dead Giveaway Mystery Game API!</p>
        <ul>
            <li><a href="/api/schema/swagger/">API Documentation (Swagger)</a></li>
            <li><a href="/api/schema/redoc/">API Documentation (ReDoc)</a></li>
            <li><a href="/admin/">Admin Panel</a></li>
        </ul>
    </body>
    </html>
    """)

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/cases/", CaseCreateAPIView.as_view()),
    path("api/cases/<int:pk>/", CaseDetailAPIView.as_view()),
    path("api/cases/<int:pk>/guess/", GuessAPIView.as_view()),

    # drf_spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
]
