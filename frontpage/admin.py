from django.contrib import admin
from .models import User, Client, Task, Assign, Draft, CommentTask

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Task)
admin.site.register(Assign)
admin.site.register(Draft)
admin.site.register(CommentTask)
#admin.site.register(CommentDraft)
