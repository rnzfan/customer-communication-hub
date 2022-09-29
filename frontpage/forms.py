from django.forms import ModelForm, Textarea, HiddenInput
from .models import CommentTask, Draft


class NewCommentTaskForm(ModelForm):
    class Meta:
        model = CommentTask
        fields = ["content"]
        widgets = {
			"content": Textarea(attrs={"placeholder": "Comment..", "rows": "4", "cols": "40", "class": "comment_task_form"})
		}
        labels = {
            "content": ""
        }
        
class DraftForm(ModelForm):
    class Meta:
        model = Draft
        fields = ["title", "content"]
        widgets = {
			"content": Textarea(attrs={"rows": "20", "cols": "10", "class": "draft_form"})
		}
        labels = {
            "title": "Title",
            "content": "Body"
        }
        
        

