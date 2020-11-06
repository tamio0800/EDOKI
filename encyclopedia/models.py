from django.db import models

# Create your models here.
class entry_profile(models.Model):
    title = models.CharField(max_length=50)  # 以title作為unique值對照好了
    content = models.TextField()
    author = models.CharField(max_length=40)
    created_time = models.DateTimeField(auto_now_add=True)
    read_times = models.IntegerField(default=0)
    last_read = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
        return self.title

class entry_edited_log(models.Model):
    entry_profile_id = models.IntegerField()
    edited_by = models.CharField(max_length=40)
    edited_time = models.DateTimeField(auto_now_add=True)
    previous_title = models.CharField(max_length=50)
    current_title = models.CharField(max_length=50)
    previous_content = models.TextField()
    current_content = models.TextField()
    def __str__(self):
        return str(self.entry_profile_id)
    
