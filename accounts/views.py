from django.shortcuts import render,reverse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView,CreateView
from .forms import SignUpForm
from photo.models import Photo
from .models import Profile,FollowerRelation
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class BaseView(View):
    @staticmethod
    def response(data={},message="",status=200):
        result = {
            "data": data,
            "message": message,
        }
        return JsonResponse(result,status)

def SignUp(request):
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            user_instance = signup_form.save(commit=False)# 밑에 저장이 있으므로 commit false
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            # Profile.objects.create(user=user_instance,nick_name="없음")
            return render(request,"accounts/signup_complete.html",{"username":user_instance.username})

    else:
        signup_form = SignUpForm()

    return render(request,"accounts/signup.html",{"form":signup_form.as_p})

@method_decorator(login_required,name="dispatch")
class ProfileView(DetailView):
    context_object_name = "profile_user"
    model= User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_posts = Photo.objects.filter(author=self.get_object())
        context['object_posts'] = object_posts
        context['post_numbers'] = object_posts.count()
        try:
            followers = FollowerRelation.objects.get(follower=self.get_object()).followee.all() # 팔로잉
            context['followees'] = followers
            context['followees_ids'] = list(followers.values_list('id',flat=True))
            context['request_usr_follow'] = FollowerRelation.objects.get(follower=user).followee.all()
        except FollowerRelation.DoesNotExist:
            pass

        context["object_followers"] = FollowerRelation.objects.select_related("follower").filter(followee__in=[self.get_object()]) # 팔로워
        return context

@method_decorator(login_required,name="dispatch")
class ProfileUpdate(UpdateView):
    model = Profile
    template_name = "accounts/profile_update.html"
    fields = ["nick_name","profile_photo"]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user != request.user:
            return HttpResponseRedirect("account/profile/"+str(object.id))
        else:
            return super(ProfileUpdate,self).dispatch(request,*args,**kwargs)

class ProfileCreate(CreateView):
    model = Profile
    template_name_suffix = "_create"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user != request.user:
            return HttpResponseRedirect("account/profile/"+str(object.id))
        else:
            return super(ProfileCreate,self).dispatch(request,*args,**kwargs)

def Profilecreate_or_update(request):
    object = Profile.objects.get(user=request.user)
    if not object:
        


