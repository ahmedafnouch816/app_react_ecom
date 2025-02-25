from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views
#10
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Blog Backend APIs",
        default_version="v1",
        description="This is the documentation for the backend API",
        terms_of_service="http://mywbsite.com/policies/",
        contact=openapi.Contact(email="desphixs@gmail.com"),
        license=openapi.License(name="BSD Licence"),
    ),
    public=True,
    permission_classes = (permissions.AllowAny, )
)

urlpatterns = [
    # Userauths API Endpoints

    path('user/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='auth_register'),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view(), name='user_profile'),
    
        
   # Post Endpoints
    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/posts/<category_slug>/', api_views.PostCategoryListAPIView.as_view()),
    path('post/lists/', api_views.PostListAPIView.as_view()),
    path('post/detail/<slug>/', api_views.PostDetailAPIView.as_view()),
    path('post/like-post/', api_views.LikePostAPIView.as_view()),
    path('post/comment-post/', api_views.PostCommentAPIView.as_view()),
    path('post/bookmark-post/', api_views.BookmarkPostAPIView.as_view()),

 
    #12 13 14 
    path('author/dashnoard/stats/<user_id>/', api_views.DashboardStats.as_view()),
    path('author/dashboard/post-list/<user_id>/', api_views.DashboardPostLists.as_view()),
    path('author/dashnoard/comment-lit/', api_views.DashboardCommentLists.as_view()),
    path('author/dashnoard/noti-list/<user_id>/', api_views.DashboardNotificationsList.as_view()),
    path('author/dashnoard/noti-mark-seen/', api_views.DashboardMarkNotificationAsSeen.as_view()),
    path('author/dashnoard/reply-comment/', api_views.DashboardReplyCommentAPIView.as_view()),
    path('author/dashboard/post-create/', api_views.DashboardPostCreateAPIView.as_view()),

    path('author/dashboard/post-detail/<user_id>/<post_id>', api_views.DashboardPostEditAPIView.as_view()),




]