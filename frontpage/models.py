from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class Client(models.Model):
    company_name = models.CharField(max_length=64)
    company_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.company_name}"


class Task(models.Model):
    title = models.CharField(max_length=64)
    gmail_id = models.CharField(max_length=64)
    snippet = models.TextField(blank=True)
    content = models.TextField(blank=True)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    time_received = models.DateTimeField(default=timezone.now)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title}"


class Assign(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="being_assigned")
    
    def __str__(self):
        return f"{self.task.title} is assigned to {self.member}"


class Draft(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="drafted_for")
    last_modified = models.DateTimeField(auto_now=True)
    #is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title}"


class CommentTask(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_commented = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ["-time_commented"]
    
    def __str__(self):
        return f"{self.task.title} - {self.member}"

