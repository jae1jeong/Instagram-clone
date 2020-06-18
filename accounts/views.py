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
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse

@method_decorator(csrf_exempt,name="dispatch")
class BaseView(View):
    @staticmethod
    def response(data={},message="",status=200):
        result = {
            "data": data,
            "message": message,
        }
        return JsonResponse(result,status)

def SignUp(request):
    '''회원가입 자동으로 프로필 객체 생성'''
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            user_instance = signup_form.save(commit=False)# 밑에 저장이 있으므로 commit false
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            user_profile = Profile.objects.create(user=user_instance, profile_photo="/default_user.jpg")
            user_profile.save()
            return render(request,"accounts/signup_complete.html",{"username":user_instance.username})


    else:
        signup_form = SignUpForm()

    return render(request,"accounts/signup.html",{"form":signup_form.as_p})

@method_decorator(login_required,name="dispatch")
class ProfileView(DetailView):
    '''프로필 뷰'''
    context_object_name = "profile_user"
    model= User
    template_name = "accounts/profile.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_posts = Photo.objects.filter(author=self.get_object())
        context['object_posts'] = object_posts
        context['post_numbers'] = object_posts.count()
        try:
            request_user_following = list(
                FollowerRelation.objects.get(follower=user).followee.all().values_list("id", flat=True))
            context["request_user_following"] = request_user_following
        except:
            pass
        try:
            followers = FollowerRelation.objects.get(follower=self.get_object()).followee.all() # 팔로잉
            context['followees'] = followers
            context['followees_ids'] = list(followers.values_list('id',flat=True)) #프로필에 있는 유저가 팔로우하는 사람들

        except FollowerRelation.DoesNotExist:
            pass

        context["object_followers"] = FollowerRelation.objects.select_related("follower").filter(followee__in=[self.get_object()]) # 팔로워
        return context

@method_decorator(login_required,name="dispatch")
class ProfileUpdate(UpdateView):
    '''프로필 업데이트'''
    model = Profile
    template_name = "accounts/profile_update.html"
    fields = ["nick_name","profile_photo"]
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.user != request.user:
            return HttpResponseRedirect(str(request.user.id))
        else:
            return super(ProfileUpdate,self).dispatch(request,*args,**kwargs)


@method_decorator(login_required,name="dispatch")
class RelationCreate(BaseView):
    '''
     follow unfollow 기능 한번 누르면 팔로우 또 한 번 누르면 언팔
    '''
    def get(self,request,*args,**kwargs):
        if "pk" in kwargs:
            user = request.user
            user_id = kwargs["pk"]
            try:
                relation = FollowerRelation.objects.get(follower=user)
            except FollowerRelation.DoesNotExist:
                relation = FollowerRelation.objects.create(follower=user)

            followees = list(FollowerRelation.objects.filter(follower=user).values_list('followee__id', flat=True))

            if user.id in followees:
                relation.followee.remove(user)
            if user_id in followees:
                relation.followee.remove(user_id)
            else:
                relation.followee.add(user_id)

        referer_url = request.META.get("HTTP_REFERER")
        path = urlparse(referer_url).path
        return HttpResponseRedirect(path)


