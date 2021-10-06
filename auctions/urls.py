from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>",views.display_listing, name="onelisting"),
    path("listing/<int:listing_id>",views.addtowatch, name="addtowatch"),
    path("listing/<int:listing_id>",views.removefromwatch, name="removefromwatch"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cat_name>/listings", views.category_listings, name="categorylistings"),
    path("watchlist/<int:user_id>",views.watchlist, name="watchlist"),
    path("watchlist/<int:user_id>/<int:listing_id>",views.remove_from_watchlist, name="remove_from_watchlist")
]
