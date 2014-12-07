#coding:utf-8
from django.db                  import models
from django.utils.translation   import ugettext_lazy as _
from django.contrib.auth.models import User

# from redactor.fields import RedactorField
from DjangoUeditor.models import UEditorField

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
        return ('category', (), {'pk': self.pk})

    @property
    def count(self):
        return self.post_set.all().count()


class Post(TimeStampedModel):
    title = models.CharField(max_length=128,verbose_name=_('title'))
    author = models.ForeignKey(User,related_name='post_author',verbose_name=_('author'))
    category = models.ForeignKey(Category,blank=True,null=True,verbose_name=_("category"))
    # content = models.TextField(verbose_name=_('content'))
    # content  = RedactorField(
    #     verbose_name=_("content"),
    #     redactor_options={'focus':'true'},
    #     upload_to='uploads/',
    #     allow_file_upload=True,
    #     allow_image_upload=True
    # )
    content=UEditorField(verbose_name=_('content'),width=800, height=300,
        toolbars="full", imagePath="images/", filePath="files/", upload_settings={"imageMaxSize":1204000},
        settings={})

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post', (), {'pk': self.pk})


class FriendLink(TimeStampedModel):
    name = models.CharField(max_length=128,unique=True,verbose_name=_("link name"))
    url  = models.URLField()

    def __unicode__(self):
        return "%s" %(self.name)

    class Meta:
        ordering = ('id',)