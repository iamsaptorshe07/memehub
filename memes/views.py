from django.shortcuts import render,redirect
from memes.models import Meme
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from memes.forms import MemePhotoForm,MemeVideoForm,MemeTextForm
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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