import xadmin
from .models import Articel,Tag


# Register your models here.
xadmin.site.register(Articel)
xadmin.site.register(Tag)