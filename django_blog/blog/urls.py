from django.urls import path
from . import views

# Define the namespace for the blog app. This is used when linking (e.g., {% url 'blog:post_list' %})
app_name = 'blog'

urlpatterns = [
    # The root path of the site, handled by the blog app.
    # This URL matches the empty string ('') because it's included at the project root level.
    path('', views.post_list, name='post_list'),
]
