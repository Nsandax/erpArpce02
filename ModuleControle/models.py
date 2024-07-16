from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class CubesViewerModel(models.Model):
    """
    Base class for Cubes Viewer stored objects.
    """

    create_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True)
    #create_user = models.ForeignKey(User)
    #update_user = models.ForeignKey(User)

    class Meta:
        abstract = True


class CubesView(CubesViewerModel):
    """
    Saved CubesViewer view.
    """

    name = models.CharField("Name", max_length=200)
    data = models.TextField()
    owner = models.ForeignKey(User,  on_delete = models.SET_NULL, related_name="user_of_cubesview", null = True, blank = True)
    shared = models.BooleanField(default = False)

    def __unicode__(self):
        return str(self.id) + " " + self.name

    class Meta:
        ordering = ['name']