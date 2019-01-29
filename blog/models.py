from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from PIL import Image

def upload_location(instance, filename):
	return "%s/%s" % (instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location,
    						  default=None,blank=True,
    						  width_field='width_field',
    						  height_field='height_field' 
    	)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    date_posted = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
    	return self.title

    def __str__(self):
        return '%s %s' % (self.id, self.title)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug':self.slug})

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()	
	if exists:
		new_slug = '%s-%s' % (slug, qs.first().id) 
		return create_slug(instance, new_slug=new_slug)
	return slug
	
def pre_post_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_post_save_reciever, sender=Post)