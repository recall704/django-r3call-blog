#coding:utf-8
import re
from django.db                  import models
# from django.utils.translation   import ugettext_lazy as _
from django.utils.translation   import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from tagging.fields import       TagField
from tagging.models import       Tag


def u_slugify(txt):
        """A custom version of slugify that retains non-ascii characters. The purpose of this
        function in the application is to make URLs more readable in a browser, so there are 
        some added heuristics to retain as much of the title meaning as possible while 
        excluding characters that are troublesome to read in URLs. For example, question marks 
        will be seen in the browser URL as %3F and are thereful unreadable. Although non-ascii
        characters will also be hex-encoded in the raw URL, most browsers will display them
        as human-readable glyphs in the address bar -- those should be kept in the slug."""
        txt = txt.strip() # remove trailing whitespace
        txt = re.sub('\s*-\s*','-', txt, re.UNICODE) # remove spaces before and after dashes
        txt = re.sub('[\s/]', '-', txt, re.UNICODE) # replace remaining spaces with underscores
        txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE) # replace colons between numbers with dashes
        txt = re.sub('"', "'", txt, re.UNICODE) # replace double quotes with single quotes
        txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]','',txt, re.UNICODE) # remove some characters altogether
        return txt



class TimeStampedModel(models.Model):
    """ TimeStampedModel
    """
    created  = models.DateTimeField(auto_now_add=True,verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True,verbose_name=_('modified'))

    class Meta:
        ordering = ('-modified', '-created',)
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=64,unique=True,verbose_name=_("category name"))

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "%s" %(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('category',(),{'pk': self.pk,'name':u_slugify(self.name)})

    @property
    def count(self):
        return self.post_set.all().count()


class Post(TimeStampedModel):
    P_TYPE_CHOICES = (
        (1,_("original")),   # 原创
        (2,_("reproduce")),  # 转载
        (3,_("sum-up")),     # 总结
        (4,_("translation")),     # 翻译
        )
    title    = models.CharField(max_length=128,verbose_name=_('title'))
    author   = models.ForeignKey(User,related_name='post_author',verbose_name=_('author'))
    category = models.ForeignKey(Category,blank=True,null=True,verbose_name=_("category"))
    tags     = TagField(blank=True,null=True)
    content  = models.TextField(verbose_name=_('content'))
    p_type   = models.IntegerField(choices=P_TYPE_CHOICES,default=1,verbose_name=_("type"))

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.title

    @property
    def is_type_original(self):
        if self.p_type == 1:
            return True
        else:
            return False
    def is_type_reproduce(self):
        if self.p_type == 2:
            return True
        else:
            return False
    def is_type_sum_up(self):
        if self.p_type == 3:
            return True
        else:
            return False

    # @models.permalink
    def get_absolute_url(self):
        # return ('post', (), {'pk': self.pk,'title':u_slugify(self.title)})
        return reverse('post',args=[self.id,u_slugify(self.title)])

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" %(content_type.app_label,content_type.model),args=(self.id,))

    @property
    def next(self):
        if Post.objects.filter(id__gt=self.id).exists():
            return Post.objects.filter(id__gt=self.id).order_by('id')[0]
        else:
            return None

    @property
    def previous(self):
        if Post.objects.filter(id__lt=self.id).exists():
            return Post.objects.filter(id__lt=self.id).order_by('-id')[0]
        else:
            return None

    def _get_ptags(self):
        return Tag.objects.get_for_object(self)
    def _set_ptags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)
    ptags = property(_get_ptags, _set_ptags)

class FriendLink(TimeStampedModel):
    name = models.CharField(max_length=128,unique=True,verbose_name=_("link name"))
    url  = models.URLField()

    def __unicode__(self):
        return "%s" %(self.name)

    class Meta:
        ordering = ('id',)