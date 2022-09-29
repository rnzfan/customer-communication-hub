import json, copy
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView
)
from .models import Draft, User, Task, Client, Assign
from .forms import DraftForm, NewCommentTaskForm
from .gmail import refreshEmails, sendEmail

from django.core.exceptions import ObjectDoesNotExist


# Global variable to store the emails from Gmail
mails = []


class TaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.select_related("being_assigned", "drafted_for").all() # Reduce the Hits to database
    context_object_name = "tasks"
    ordering = ["-time_received"]
    paginate_by = 6
    
    def get(self, request, *args, **kwargs):
        startup()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        page_number = request.POST.get("page_number")
        if "comment_task_button" in request.POST:
            filledTaskForm = NewCommentTaskForm(request.POST)
            task_id = request.POST.get("comment_task_button")   
            if filledTaskForm.is_valid():
                new_comment_task = filledTaskForm.save(commit=False)
                new_comment_task.member = request.user
                new_comment_task.task = Task.objects.get(id=task_id)
                new_comment_task.save()
                return HttpResponseRedirect(reverse("task", args=[task_id]) + f"?page={page_number}")
            else:
                return render(request, "frontpage/task_list.html", {
                    "message": "Invalid form submission!"
                })
        if "draft_save_button" in request.POST:
            task_id = request.POST.get("draft_save_button")
            current_task = Task.objects.get(id=task_id)
            try:
                saved_draft = Draft.objects.get(task=current_task)
            except ObjectDoesNotExist:
                saved_draft = None
                
            if saved_draft:
                draft = DraftForm(request.POST, instance=saved_draft)
                draft.save()
            else:
                new_filled_draft = DraftForm(request.POST)
                if new_filled_draft.is_valid():
                    new_draft = new_filled_draft.save(commit=False)
                    new_draft.task = current_task
                    new_draft.save()
                else:
                    return render(request, "frontpage/task_list.html", {
                        "message": "Invalid form submission!"
                    })
                    
            return HttpResponseRedirect(reverse("task", args=[task_id]) + f"?page={page_number}")
        if "draft_send_button" in request.POST:
            task_id = request.POST.get("draft_send_button")
            current_task = Task.objects.get(id=task_id)
            
            message = sendEmail({
                "to": current_task.client.company_email,
                "title": current_task.drafted_for.title,
                "content": current_task.drafted_for.content
            })
            if (message):
                print(message)
                current_task.is_done = True
                current_task.save()
            return HttpResponseRedirect(reverse("task", args=[task_id]) + f"?page={page_number}")
                
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.all()
        context["comment_form"] = NewCommentTaskForm()
        
        # To avoid keyError
        if self.kwargs != {}:
            task_id = self.kwargs["task_id"]
        else:
            task_id = None
        context["current_task"] = task_id
        
        # Assign each draft form to its own task
        for task in context["object_list"]:
            try:
                task.draft_form = DraftForm(instance=task.drafted_for)
                    
            except ObjectDoesNotExist:
                task.draft_form = DraftForm({"title": f"Re: {task.title}"})
                
        return context


class UserTaskListView(TaskListView):
    
    def get_queryset(self):
        return Task.objects.select_related("being_assigned", "drafted_for").filter(
            being_assigned__member=self.request.user
        )
        
            
class UnassignedTaskListView(TaskListView):
    
    def get_queryset(self):
        return Task.objects.select_related("being_assigned", "drafted_for").filter(
            being_assigned__isnull=True
        )
        

# To sync with Gmail when starting this web app
def startup():
    # Deep copy the list to store the previous status
    previous_mails = copy.deepcopy(mails)
    # Reload all new emails
    refreshEmails(mails)
    # Update only the new emails
    new_mails = [ m for m in mails if m not in previous_mails ]
    for mail in new_mails:
        if mail["gmail_id"] not in Task.objects.all().values_list("gmail_id", flat=True):
            new_task = Task.objects.create(title=mail["subject"],
                                           content=mail["message"],
                                           snippet=mail["snippet"],
                                           gmail_id=mail["gmail_id"])
            try: 
                new_task.client = Client.objects.get(company_email=mail["from"])
            except ObjectDoesNotExist:
                print("There is a task from outside of the client list!")
            finally:
                new_task.save()


@login_required
def assign(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.get(id=data.get("task_id"))
        member = User.objects.get(id=data.get("member_id"))
        assignment = Assign(
            member = member,
            task = task
        )
        assignment.save()
        return JsonResponse({"message": f"{member} has been assigned to {task}."}, status=201)


@login_required
def unassign(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = Task.objects.get(id=data.get("task_id"))
        Assign.objects.get(task=task).delete()
        return JsonResponse({"message": f"{task} is unassigned"}, status=201)
         

# Below views handle login, logout, register
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tasks"))
        else:
            return render(request, "frontpage/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "frontpage/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "frontpage/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "frontpage/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "frontpage/register.html")