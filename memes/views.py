from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from memes.models import Meme,Comment
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from memes.forms import MemePhotoForm,MemeVideoForm,MemeTextForm
from django.views.generic import DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from memes.templatetags import extras

# Create your views here.

def index(request):
	memes = Meme.objects.all().order_by('-created_date')
	return render(request,'index.html',{'memes': memes})
    
@login_required
def profile(request):
    user = UserProfile.objects.get(email=request.user)
    memes = Meme.objects.filter(author=user).order_by('-created_date')
    return render(request,'user/profile.html',{'memes': memes})

@login_required  
def profile_update(request):
    user=UserProfile.objects.get(email=request.user)
    if request.method == 'POST':
        name = request.POST.get('name').capitalize()        
        user.name=name
        user.save()
        messages.success(request,"Profile Updated")
        return redirect('/profile')
    return render(request,'user/profile_update.html')


class MemeTextCreateView(LoginRequiredMixin, CreateView):
    model = Meme
    template_name = 'memes/meme_text_form.html'
    fields = ['meme_text']
    success_url = '/profile'

    def form_valid(self, MemeTextForm):
        MemeTextForm.instance.author = self.request.user
        messages.success(self.request,'Text Meme added')
        return super().form_valid(MemeTextForm)

class MemePhotoCreateView(LoginRequiredMixin, CreateView):
    model = Meme
    template_name = 'memes/meme_photo_form.html'
    fields = ['photos','caption']
    success_url = '/profile'

    def form_valid(self, MemePhotoForm):
        MemePhotoForm.instance.author = self.request.user
        messages.success(self.request,'Photo Meme added')
        return super().form_valid(MemePhotoForm)

class MemeVideoCreateView(LoginRequiredMixin, CreateView):
    model = Meme
    template_name = 'memes/meme_video_form.html'
    fields = ['videos','caption']
    success_url = '/profile'

    def form_valid(self, MemeVideoForm):
        MemeVideoForm.instance.author = self.request.user
        messages.success(self.request,'Video Meme added')
        return super().form_valid(MemeVideoForm)

class MemeDetailView(DetailView):
    model = Meme
    template_name = 'memes/meme_details.html'
    context_object_name = 'meme'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(meme=self.get_object(),parent=None).order_by('-date_posted')
        replies = Comment.objects.filter(meme=self.get_object()).exclude(parent=None).order_by('-date_posted')
        replyDict= {}
        for reply in replies:
              if reply.parent.id not in replyDict.keys():
                   replyDict[reply.parent.id]=[reply]
              else:
                   replyDict[reply.parent.id].append(reply)
        data['comments'] = comments
        data['replyDict'] = replyDict
        return data

@login_required   
def postComment(request):
    if request.method == 'POST':
          content = request.POST.get('content')
          user = request.user
          meme_id = request.POST.get('meme_id')
          meme = Meme.objects.get(pk=meme_id)
          parent_id = request.POST.get('parent_id')
          if parent_id == " ":
               comment = Comment(content=content,user=user,meme=meme)
               comment.save()
               messages.success(request,"Your comment posted")
          else: 
               parent = Comment.objects.get(pk=parent_id)
               comment = Comment(content=content,user=user,meme=meme,parent=parent)     
               comment.save()
               messages.success(request,"Your reply posted")
    return redirect(f"/memes/{meme.id}") 

#######################
# Likes
@login_required
def meme_likes(request):
    user = request.user
    if request.method == 'POST':
        meme_id = request.POST.get('meme_id')
        meme_like = Meme.objects.get(pk=meme_id)
        meme_dislike = Meme.objects.get(pk=meme_id)
        if user in meme_like.likes.all():
            meme_like.likes.remove(user)
            return HttpResponseRedirect(f'/memes/{meme_id}')    
        else:
            if user in meme_dislike.dislikes.all():#jump from dislike to like
                meme_dislike.dislikes.remove(user)
                meme_like.likes.add(user)
                return HttpResponseRedirect(f'/memes/{meme_id}')
            meme_like.likes.add(user)
        return HttpResponseRedirect(f'/memes/{meme_id}')
@login_required        
def meme_dislikes(request):
    user = request.user
    if request.method == 'POST':
        meme_id = request.POST.get('meme_id')
        meme_like = Meme.objects.get(pk=meme_id)
        meme_dislike = Meme.objects.get(pk=meme_id)
        if user in meme_dislike.dislikes.all():
            meme_dislike.dislikes.remove(user)    
            return HttpResponseRedirect(f'/memes/{meme_id}')  
        else:
            if user in meme_like.likes.all():#jump from like to dislike
                meme_like.likes.remove(user)
                meme_dislike.dislikes.add(user)
                #create reaction
                return HttpResponseRedirect(f'/memes/{meme_id}')
            #else:
            meme_dislike.dislikes.add(user)
            #create reaction    
        return HttpResponseRedirect(f'/memes/{meme_id}')
#######################
# comment update
@login_required
def comment_update(request,id):
    if request.method == 'POST':
        comment = request.POST.get('content')
        obj = Comment.objects.get(pk=id)
        meme = Meme.objects.get(pk=obj.meme.id)
        if comment == "":
            messages.error(request,"This Comment is blank")
            return redirect(f'/memes/{meme.id}')
        if comment == obj.content:
            messages.error(request,"This Comment update isn't allowed")
            return redirect(f'/memes/{meme.id}')    
        obj.content = comment
        obj.save()
        messages.success(request,"Comment updated successfully")
        return redirect(f'/memes/{meme.id}')
@login_required
def comment_delete(request,id):
    comment = Comment.objects.get(pk=id)
    meme = Meme.objects.get(pk=comment.meme.id)
    comment.delete()
    messages.success(request,'Comment deleted')
    return redirect(f'/memes/{meme.id}')

#######################
# reply update
@login_required
def reply_update(request,id):
    if request.method == 'POST':
        reply = request.POST.get('content')
        obj = Comment.objects.get(pk=id)
        meme = Meme.objects.get(pk=obj.meme.id)
        if reply == "":
            messages.error(request,'Reply is blank')
            return redirect(f'/memes/{meme.id}')
        if reply == obj.content:
            messages.error(request,"This reply update isn't allowed")
            return redirect(f'/memes/{meme.id}')    
        obj.content = reply
        obj.save()
        messages.success(request,"Reply updated successfully")
        return redirect(f'/memes/{meme.id}')
@login_required        
def reply_delete(request,id):
    reply = Comment.objects.get(pk=id)
    meme = Meme.objects.get(pk=reply.meme.id)
    reply.delete()
    messages.success(request,'Reply deleted')
    return redirect(f'/memes/{meme.id}')        