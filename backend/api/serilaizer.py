from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models as api_models




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Personnalise le contenu du token JWT généré pour un utilisateur.

        Cette méthode surcharge `get_token` de la classe parent `TokenObtainPairSerializer`.
        Elle permet d'ajouter des informations supplémentaires (comme `full_name`, `email`,
        et `username`) au payload du token JWT.

        Arguments :
        - cls : Référence à la classe actuelle (`MyTokenObtainPairSerializer`).
        - user : Instance de l'utilisateur pour lequel le token est généré.

        Retour :
        - token : Instance du token enrichi avec des champs personnalisés.
        """
        # Appel de la méthode `get_token` de la classe parent pour générer un token de base.
        token = super().get_token(user)

        # Ajout de champs personnalisés au payload du token.
        token['full_name'] = user.full_name  # Ajoute le nom complet de l'utilisateur.
        token['email'] = user.email          # Ajoute l'adresse e-mail de l'utilisateur.
        token['username'] = user.username    # Ajoute le nom d'utilisateur.

        # Retourne le token enrichi.
        return token 

    

class RegisterSerialier(serializers.ModelSerializer):
    # Field for password with write-only access and validation
    password = serializers.CharField(write_only=True, required=True , validators=[validate_password]) 
    # Field for confirming password with write-only access
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = api_models.User
        fields = ['full_name', 'email', 'username', 'password', 'password2']
    
    #Validate that the password and confirm password fields match.    
    def validate(self, attr):
        if attr['password'] != attr['password']:
            raise serializers.ValidationError({"password": "Password field didn't match"})
        return attr

    def create(self , validated_data):
        user = api_models.User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email'],
        )
        
        email_username, mobile = user.email.split("@")
        user.username = email_username
        # Set the user's password based on the validated data
        user.set_password(validated_data['password'])
        user.save()
        
        return user 
    
    
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = '__all__'
        
        
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Profile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response
        
        
class CategorySerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.posts.count()
    
    class Meta:
        model = api_models.Category
        fields = ["id", "title", "image", "slug" , "post_count"]

#
class CommentSerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.posts.count()
    
    class Meta:
        model = api_models.Comment
        fields = '__all__'
        
        def __int__(self,*args, **kwargs):
            super(CommentSerializer, self).__init__(*args,**kwargs)
            request =  self.context("request")
            if request and request.method == "POST":
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1
                
                
#
class PostSerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.posts.count()
    
    class Meta:
        model = api_models.Post
        fields = '__all__'
        
        def __int__(self,*args, **kwargs):
            super(PostSerializer, self).__init__(*args,**kwargs)
            request =  self.context("request")
            if request and request.method == "POST":
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1        
                
#
class BookmarkSerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.posts.count()
    
    class Meta:
        model = api_models.Bookmark
        fields = '__all__'
        
        def __int__(self,*args, **kwargs):
            super(BookmarkSerializer, self).__init__(*args,**kwargs)
            request =  self.context("request")
            if request and request.method == "POST":
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1           
                
#
class NotificationSerializer(serializers.ModelSerializer):
    def get_post_count(self, category):
        return category.posts.count()
    
    class Meta:
        model = api_models.Notification
        fields = '__all__'
        
        def __int__(self,*args, **kwargs):
            super(NotificationSerializer, self).__init__(*args,**kwargs)
            request =  self.context("request")
            if request and request.method == "POST":
                self.Meta.depth = 0
            else:
                self.Meta.depth = 1        
                   
                   
                   

class AuthorSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(default=0)
    posts = serializers.IntegerField(default=0)
    likes = serializers.IntegerField(default=0)
    books = serializers.IntegerField(default=0)
