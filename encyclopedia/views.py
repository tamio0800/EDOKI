import re
import random
import markdown2
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render as _render, redirect
from django.contrib import messages
from django.urls import reverse
from functools import wraps
from . import util
from django.contrib.auth.decorators import login_required
import datetime
from encyclopedia.models import entry_profile, entry_edited_log

def get_username(a_request_obj):
    username = None
    if a_request_obj.user.is_authenticated:
        username = a_request_obj.user.username
    return username

@login_required(login_url='account/login/')
def render(req, url, extra={}):
    """
    Hooking into render functionality and dynamically
    making entries list available for all views
    """
    alphabet_list = list(map(chr, range(65, 65 + 26)))
    extra.update(entries_options=util.list_entries(), 
    alphabet_list=alphabet_list,
    debug=settings.DEBUG)

    return _render(req, url, extra)

@login_required(login_url='account/login/')
def referred_message(req, url, msg, level="success"):
    """Handle referred message  when a view is redirect

    Arguments:
        req [dict] -- redirect request object
        url [str]  --  referred url
        msg [str]  -- message to display
        level[str] -- message level. default: success
    """
    referred_url = req.META.get("HTTP_REFERER")
    if referred_url and url in referred_url:
        # dynamically creating message with specified level
        msg_type = getattr(messages, level, None)
        if msg_type:
            msg_type(req, msg)

@login_required(login_url='account/login/')
def index(request):
    username = get_username(request)
    if request.META.get('PATH_INFO', None) == '/':
        return redirect('index')

    entry_list = util.list_entries()
    entry_read_times_combined_list = list()
    if request.method == "POST":
        letter = request.POST.get("letter")
        search = request.POST.get("search")
        # Handles searches from index sidebar
        if search is not None:
            search = search.lower().strip()
            for entry in entry_list:
                if search == entry.lower():
                    return redirect("wiki_entry", title=entry)

            entry_list = list(filter(lambda x: search in x.lower(), entry_list))
            if not entry_list:
                return redirect(notFound)

        # Handles A-Z sorted list in index main
        elif letter is not None:
            # map all letter and entry to lowercase
            letter = letter.strip().lower()
            # filter by entries starting with "letter"
            entry_list = list(
                filter(lambda x: x.lower().startswith(letter), entry_list)
            )

    entry_read_times_combined_list = list()
    for each_entry_title in entry_list:
        read_times = entry_profile.objects.filter(title=each_entry_title).first().read_times
        entry_read_times_combined_list.append(
            {'entry':each_entry_title, 'read_times':'{:,}'.format(read_times)} 
        )

    context = {
        "entries": entry_list, 
        'username': username, 
        'entry_read_times_combined_list': entry_read_times_combined_list}
    return render(request, "encyclopedia/index.html", context)

@login_required(login_url='account/login/')
def wiki_entry(request, title):
    """ Base wiki view to view all available entries"""
    username = get_username(request)
    context = {}
    entry_list = util.list_entries()

    # Filter the title  with case-insensitive search
    title = title.strip()
    wiki = [entry for entry in entry_list if title.lower() in entry.lower()]

    if not wiki or wiki is None:
        return redirect(notFound)

    # get Entry by its title
    entry = util.get_entry(wiki[0])
    context["title"] = title
    context["entry"] = markdown2.markdown(entry).strip()
    context["username"] = username
    post_by = username
    post_time = str(datetime.datetime.now()).split('.')[0]
    
    entry_logs = list()
    entry_profile_query = entry_profile.objects.filter(title=title).first()
    autor = entry_profile_query.author
    editor_and_time_lists = entry_edited_log.objects.filter(entry_profile_id=entry_profile_query.id).order_by('-edited_time').values_list('edited_by', 'edited_time')
    if len(editor_and_time_lists) > 0:
        for each_editor_and_time_list in editor_and_time_lists:
            editor, edited_time = each_editor_and_time_list[0], str(each_editor_and_time_list[1] + datetime.timedelta(hours=8)).split('.')[0].replace('-', '.')
            entry_logs.append('edited by ' + editor + '@' + edited_time)
    entry_logs.append('created by ' + autor + '@' + str(entry_profile_query.created_time + datetime.timedelta(hours=8)).split('.')[0].replace('-', '.'))

    context["entry_logs"] = entry_logs

    entry_profile_query = entry_profile.objects.filter(title=title).first()
    setattr(entry_profile_query, 'read_times', entry_profile_query.read_times + 1)
    entry_profile_query.save()

    return render(request, "encyclopedia/base_entry.html", context)

@login_required(login_url='account/login/')
def saveHandler(request, **kwargs):
    """Save Entry

    Arguments:
        request {obj} -- Django request

    Returns:
        [Django redirect] -- redirect view   'index/' or 'wiki/<title>'
    """
    # This view handle saving new and edit entries
    title = kwargs.get("title", "")
    content = kwargs.get("content", "")
    if content and title:
        title = title.strip()
        # re.sub(r"\s", "_", title.strip())
        entry = util.save_entry(title.strip(), str(content).strip())
        return redirect("wiki_entry", title=title)
    return redirect(notFound)

@login_required(login_url='account/login/')
def create_update(request, title=""):
    username = get_username(request)
    """Creates or updates wiki entry

    Arguments:
        request {obj} -- Django request
        title {str} -- Name of Wiki entry to update

    Returns:
        [Django view] -- rendered view template 'edit-entry/'
    """

    context = {"config": "create"}
    previous_title = title
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submit = request.POST.get("submit")
        hidden = request.POST.get("config")
        author = get_username(request)

        if submit is None:
            # User cancelled request
            if "create" in hidden:
                # Cancelled creating - redirect to index
                return redirect(index)
            else:
                # Cancelled updating - redirect to wiki entry
                return redirect(reverse("wiki_entry", kwargs={"title": title}))
        elif not title or not content:
            # Submitted but no content was added.
            # (mainly for creation since update already have content)
            # Redirect user to the same page to make changes
            messages.warn(
                request, f" You must add a title and content to create entry!"
            )
            return render(request, "encyclopedia/create_edit_entry.html", context)

        # Setup saving the entry
        action = "updated" if "edit" in hidden else "created"
        if action == "updated":
            # delete previous entry
            util.delete_entry(previous_title)
            # 找到原始的文章id
            entry_info_query = entry_profile.objects.filter(title=previous_title).first()
            entry_edited_log.objects.create(
                entry_profile_id = entry_info_query.id,
                edited_by = author,
                previous_title = previous_title,
                current_title = title,
                previous_content = entry_info_query.content,
                current_content = content,
            ).save()
            setattr(entry_info_query, 'title', title)
            setattr(entry_info_query, 'content', content)
            entry_info_query.save()
        else:
            # 新建條目
            entry_profile.objects.create(
                title = title,
                content = content,
                author = author,
            ).save()
        messages.success(request, f" Your entry was {action} successfully!")
        

        return saveHandler(request, title=title, content=content)

    else:  # GET Request
        context = {"config": "create"}  # default value
        context["username"] = username
        if title:
            entry = util.get_entry(title)
            if not entry or entry is None:
                return redirect(notFound)
            context["entry"] = entry
            context["config"] = "edit"

        # Convert entry from html to Markdown
        context.update(
            {
                "title": title,
                "unavailable_entry": util.list_entries(),
            }
        )
    return render(request, "encyclopedia/create_edit_entry.html", context)

@login_required(login_url='account/login/')
def random_entry(request):
    username = get_username(request)
    """Random Wiki entry

    Arguments:
        request {obj} -- Django request

        Returns:
            [Django view] -- rendered view template   'delete-entry/'
    """

    entry_list = util.list_entries()
    if entry_list:
        rand_entry = random.choices(entry_list)[0]
        return HttpResponseRedirect(reverse("wiki_entry", args=(rand_entry,)))

    messages.error(request, f"Opp... Something went wrong!")
    return redirect(index)

@login_required(login_url='account/login/')
def delete_entry(request, title, deletion=None):
    username = get_username(request)
    """Delete Wiki entry

    Arguments:
        request {obj} -- Django request
        title {str} -- Name of entry to detete

    Returns:
        [Django view] -- rendered view template   'delete-entry/'
    """

    context = {"username": username}
    if deletion:
        if title:
            if deletion == "delete":
                util.delete_entry(title)
                messages.error(request, f"{title} was deleted.")
                return redirect("index")
            else:
                messages.warning(request, f"Deleting was cancel {title}.")
                return redirect("wiki_entry", title=title)

    context["title"] = title
    return render(request, "encyclopedia/delete_entry.html", context)

@login_required(login_url='account/login/')
def notFound(request):
    username = get_username(request)
    return render(request, "encyclopedia/notfound.html")

@login_required(login_url='account/login/')
def handler_404(request, exception):
    username = get_username(request)
    return render(request, "encyclopedia/404.html")
