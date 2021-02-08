from django.urls import path
from memes.views import index,profile,profile_update,MemeTextCreateView,MemePhotoCreateView,MemeVideoCreateView,MemeDetailView

urlpatterns = [
    path('', index, name='index'),
    path('profile',profile,name='profile'),
    path('profile-update',profile_update,name='profile-update'),
    path('memes/text/new',MemeTextCreateView.as_view(), name='meme-text-add' ),
    path('memes/photos/new',MemePhotoCreateView.as_view(), name='meme-photo-add'),
    path('memes/videos/new',MemeVideoCreateView.as_view(), name='meme-video-add' ),
    path('memes/<int:pk>',MemeDetailView.as_view(), name='meme-detail'),
]

