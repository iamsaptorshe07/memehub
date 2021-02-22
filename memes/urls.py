from django.urls import path
from memes.views import index,profile,profile_update,MemeTextCreateView,MemePhotoCreateView,MemeVideoCreateView,MemeDetailView
from memes.views import postComment,comment_update,comment_delete,reply_update,reply_delete,meme_likes,meme_dislikes
urlpatterns = [
    path('', index, name='index'),
    path('profile',profile,name='profile'),
    path('profile-update',profile_update,name='profile-update'),
    path('memes/text/new',MemeTextCreateView.as_view(), name='meme-text-add' ),
    path('memes/photos/new',MemePhotoCreateView.as_view(), name='meme-photo-add'),
    path('memes/videos/new',MemeVideoCreateView.as_view(), name='meme-video-add' ),
    path('memes/<int:pk>',MemeDetailView.as_view(), name='meme-detail'),

    path('memes/likes',meme_likes,name=""),
    path('memes/dislikes',meme_dislikes,name=""),

    path('memes/postComment',postComment,),
    path('comment-update/<int:id>',comment_update,),
    path('comment-delete/<int:id>',comment_delete,),

    path('reply-update/<int:id>',reply_update,),
    path('reply-delete/<int:id>',reply_delete,),
]

