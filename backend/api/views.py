from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime


# Custm Imports
from api import serilaizer as api_serializer
from api import models as api_models
import json
import random

# This code defines a DRF View class called MyTokenObtainPairView, which inherits from TokenObtainPairView.
class MyTokenObtainPairView(TokenObtainPairView):
    # Here, it specifies the serializer class to be used with this view.
    serializer_class = api_serializer.MyTokenObtainPairSerializer

# This code defines another DRF View class called RegisterView, which inherits from generics.CreateAPIView.
class RegisterView(generics.CreateAPIView):
    # It sets the queryset for this view to retrieve all User objects.
    queryset = api_models.User.objects.all()
    # It specifies that the view allows any user (no authentication required).
    permission_classes = (AllowAny,)
    # It sets the serializer class to be used with this view.
    serializer_class = api_serializer.RegisterSerializer


# This code defines another DRF View class called ProfileView, which inherits from generics.RetrieveAPIView and used to show user profile view.
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = api_serializer.ProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']

        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile
    

def generate_numeric_otp(length=7):
        # Generate a random 7-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        return otp
    
#7
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        #api models as api_models 
        return api_models.Category.objects.all()


class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category, status="Active")
    
    
#8

class PostListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return api_models.Post.objects.filter(status="Active")
    
class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        post = api_models.Post.objects.get(slug=slug, status="Active")
        post.view += 1
        post.save()
        return post
    
    
#9

class LikePostAPIView(APIView):
    #pour utilise swagger auto pour tesyt comme post man 
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = api_models.User.objects.get(id=user_id)
        post = api_models.Post.objects.get(id=post_id)

        # Check if post has already been liked by this user
        if user in post.likes.all():
            # If liked, unlike post
            post.likes.remove(user)
            return Response({"message": "Post Disliked"}, status=status.HTTP_200_OK)
        else:
            # If post hasn't been liked, like the post by adding user to set of poeple who have liked the post
            post.likes.add(user)
            
            # Create Notification for Author
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type="Like",
            )
            # Return response back to the frontend
            return Response({"message": "Post Liked"}, status=status.HTTP_201_CREATED)
        

#10
class PostCommentAPIView(APIView):
    # add use swagger with different fileds 
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'comment': openapi.Schema(type=openapi.TYPE_STRING),

            },
        ),
    )
    
    def post(self, request):
       # Get data from request.data (frontend)
        post_id= request.data['post_id']
        name= request.data['name']
        email= request.data['email']
        comment= request.data['comment']
                
        # get post id  and craete           
        post =  api_models.Post.objects.get(id=post_id)
        # Create Comment
        api_models.Comment.objects.create(
            post=post,
            name=name,
            email=email,
            comment=comment
        )
        
        # Create Notification for Author
        api_models.Notification.objects.create(
            user=post.user,
            post=post,
            type="Comment",
        )
        # Return response back to the frontend
        return Response({"message": "Comment send "}, status=status.HTTP_201_CREATED)
    
#11
class BookmarkPostAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        
            },
        ),
    )
    
    def post(self, request):
         # Get data from request.data (frontend)
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        
        # Get data from api_model
        user = api_models.User.objects.get(id=user_id)
        post = api_models.Post.objects.get(id=post_id)
        
        bookmark = api_models.Bookmark.objects.filter(post=post, user=user).first()
        
        if bookmark:
            # Remove post from bookmark
            bookmark.delete()
            return Response({"message": "Post un - bookmarked "}, status=status.HTTP_200_OK)
        else:
            api_models.Bookmark.objects.create(
                user=user,
                post=post,
            ) 
            # Create Notification for Author
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type="Bookmark",
            )
        # Return response back to the frontend
        return Response({"message": "Add bookmarhed"}, status=status.HTTP_201_CREATED)

        
        
#12
######################## Author Dashboard APIs ########################
class DashboardStats(generics.ListAPIView):
    serializer_class = api_serializer.AuthorStats
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)

        views = api_models.Post.objects.filter(user=user).aggregate(view=Sum("view"))['view']
        posts = api_models.Post.objects.filter(user=user).count()
        likes = api_models.Post.objects.filter(user=user).aggregate(total_likes=Sum("likes"))['total_likes']
        bookmarks = api_models.Bookmark.objects.all().count()

        return [{
            "views": views,
            "posts": posts,
            "likes": likes,
            "bookmarks": bookmarks,
        }]
    
    def list(self, request, *args, **kwargs):
        querset = self.get_queryset()
        serializer = self.get_serializer(querset, many=True)
        return Response(serializer.data)

    

#13
class DashboardPostLists(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id =  self.kwargs['user_id']
        user =  api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.filter(user=user).order_by("-id")
class DashboardCommentLists(generics.ListAPIView):
    serializer_class = api_serializer.CommentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user_id =  self.kwargs['user_id']
        user =  api_models.User.objects.get(id=user_id)
        return api_models.Comment.objects.filter(post__user=user)
class DashboardNotificationsList(generics.ListAPIView):
    serializer_class = api_serializer.NotificationSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user_id =  self.kwargs['user_id']
        user =  api_models.User.objects.get(id=user_id)
        return api_models.Comment.objects.filter(seen=False , user=user)
class DashboardMarkNotificationAsSeen(APIView):
    def post(self, request):
        noti_id = request.data['noti_id']
        noti = api_models.Notification.objects.get(id=noti_id)
        
        noti.seen =  True 
        noti.save()
        
        return Response({"message": "Noti maked as seen"}, status=status.HTTP_200_OK)
class  DashboardReplyCommentAPIView(APIView):
    
    def post(self, request):
        comment_id =  request.data['comment_id']
        reply = request.data['reply']
        
        comment = api_models.Comment.objects.get(id=comment_id)
        comment.reply = reply
        comment.save()
        
        return Response({"message": "comment response sent "}, status=status.HTTP_201_CREATED)
#ip14

class DashboardPostCreateAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print(request)
        
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')
        
        user = api_models.User.objects.get(id=user_id)
        category = api_models.Category.objects.get(id=category_id)
        
        api_models.Post.objects.create(
            user=user, 
            titel=title,
            image=image, 
            tags=tags,
            status=post_status,
            category=category,
            description=description,
                                       )
        
        return Response({"message": "Post created successfully "}, status=status.HTTP_201_CREATED)

#ip15
class DashboardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.get(user=user, id=post_id)

    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()

        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')

        print(title)
        print(image)
        print(description)
        print(tags)
        print(category_id)
        print(post_status)

        category = api_models.Category.objects.get(id=category_id)

        post_instance.title = title
        if image != "undefined":
            post_instance.image = image
        post_instance.description = description
        post_instance.tags = tags
        post_instance.category = category
        post_instance.status = post_status
        post_instance.save()

        return Response({"message": "Post Updated Successfully"}, status=status.HTTP_200_OK)

{
    "title": "New post",
    "image": "",
    "description": "lorem",
    "tags": "tags, here",
    "category_id": 1,
    "post_status": "Active"
}