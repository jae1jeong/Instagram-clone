from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from urllib.parse import urlparse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import Photo,Comment
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.base import View
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import FollowerRelation,Profile
from django.contrib.auth import get_user_model


# def chk_requser_objuser(obj_usr,req_usr):
#     if obj_usr != req_usr:
#         return False
#     return True

class PhotoList(LoginRequiredMixin,ListView):
    # 모든 유저들의 게시글을 볼 수 있음
    login_url = "/accounts/login"
    redirect_field_name = 'redirect_to'
    model = Photo
    template_name_suffix = "_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhotoList,self).get_context_data(**kwargs)
        return context

@method_decorator(login_required,name='dispatch')
class PhotoFeed(ListView):
    # 팔로우한 사람 게시글만 볼 수 있음
    template_name_suffix = "_feed"
    model = Photo
    paginate_by = 1

    def get_context_data(self,**kwargs):
        context = super(PhotoFeed,self).get_context_data(**kwargs)
        user = self.request.user
        followees = FollowerRelation.objects.filter(follower=user).values_list("followee__id",flat=True)
        lookup_user_ids = [user.id] + list(followees)
        context['contents'] = Photo.objects.select_related("author").filter(author__id__in = lookup_user_ids)
        User = get_user_model()
        can_follow_users_list = User.objects.exclude(id__in=lookup_user_ids)
        context["can_follow_users_list"] = can_follow_users_list
        try:
            context['profile'] = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(user=user,profile_photo="/default_user.jpg")
            user_profile.save()
        return context

class PhotoCreate(LoginRequiredMixin,CreateView):
    login_url = "/accounts/login"
    redirect_field_name = 'redirect_to'
    model = Photo
    fields = ["text","image","is_public",]
    template_name_suffix = "_create"

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect("/")

@method_decorator(login_required,name='dispatch')
class PhotoUpdate(UpdateView):
    model = Photo
    fields = ["text","image"]
    template_name_suffix = "_update"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request,"수정할 권한이 없습니다.")
            return HttpResponseRedirect("/")
        else:
            return super(PhotoUpdate,self).dispatch(request,*args,**kwargs) # 업데이트문을 다시 시작하겠다.

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = "_delete"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()

        if object.author != request.user:
            messages.warning(request,"삭제할 권한이 없습니다.")
            return HttpResponseRedirect("/")
        else:
            return super(PhotoDelete,self).dispatch(request,*args,**kwargs)

class PhotoDetail(DetailView,LoginRequiredMixin):
    model = Photo
    template_name_suffix = "_detail"
    # form_class = CommentForm
    context_object_name = "post"

    def get_success_url(self): # post 처리가 성공한뒤
        return reverse("photo:detail",kwargs={"pk":self.object.pk})

    def get_context_data(self, **kwargs): # template 보낼 context 설정
        context = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(photo=self.get_object()).order_by("-comment_date")
        context['comments'] = comments_connected
        context['form'] = CommentForm(instance=self.request.user)
        return context

    def post(self,request,*args,**kwargs):
        new_comment = Comment(comment_content=request.POST.get("comment_content"),author = self.request.user,photo = self.get_object())
        new_comment.save()
        return self.get(self,request,*args,**kwargs)

class PhotoLike(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: # 로그인이 안되어있으면
            return HttpResponseForbidden()
        else:
            if "photo_id" in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get("HTTP_REFERER")
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class PhotoFavorite(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: # 로그인이 안되어있으면
            return HttpResponseForbidden()
        else:
            if "photo_id" in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)

            referer_url = request.META.get("HTTP_REFERER")
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class PhotoLikeList(ListView):
    model = Photo
    template_name = "photo/photo_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,"로그인이 필요합니다.")
            return HttpResponseRedirect("/")
        return super(PhotoLikeList,self).dispatch(request,*args,**kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = user.like_post.all()
        return queryset

class PhotoFavoriteList(ListView):
    model = Photo
    template_name = "photo/photo_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,"로그인이 필요합니다.")
            return HttpResponseRedirect("/")
        return super(PhotoFavoriteList,self).dispatch(request,*args,**kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset



#
class CommentDelete(DeleteView):
    model = Comment
    template_name_suffix = "_delete"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request,"삭제할 권한이 없습니다.")
            return HttpResponseRedirect("/")
        else:
            return super(CommentDelete,self).dispatch(request,*args,**kwargs)

