from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>",views.display_listing, name="onelisting"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cat_name>/listings", views.category_listings, name="categorylistings")
]
