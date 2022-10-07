from django.urls import path

from .views import DetailView, MyPosts, ResultsView, SignUpPage, SignInPage, PostCreate, FeedView, ExploreView, DeletePage, PostEdit
from django.contrib.auth.views import LogoutView


app_name =  'Polls'
urlpatterns = [
    path("signup/", SignUpPage.as_view(), name="sign-up"),
    path("logout/", LogoutView.as_view(next_page = 'Polls:explore'), name="logout"),
    path("accounts/login/", SignInPage.as_view(), name="sign-in"),

    path("create-post/", PostCreate.as_view(), name="create-post"),
    path("edit-post/<int:pk>/", PostEdit.as_view(), name="edit-post"),
    path("delete-post/<int:pk>/", DeletePage.as_view(), name="delete-post"),
    # ex: /polls/
    path("home/", FeedView.as_view(), name="home"),
    path("explore-page/", ExploreView.as_view(), name="explore"),
    path("home/myposts", MyPosts.as_view(), name="my-posts")
]
