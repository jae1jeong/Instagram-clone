from haystack import indexes
from .models import Profile


class ProfileIndex(indexes.SearchIndex,indexes.Indexable):
    ''' 모델을 인덱스 객체로 반환하여 검색한다 '''
    text = indexes.CharField(document=True,use_template=True,template_name="search/profile_text.txt")
    user = indexes.CharField(model_attr="user")

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

