from datetime import datetime

from django.shortcuts import render, redirect


def profile_view(request):
    username = request.session.get("username", "Гість")
    theme = request.session.get("theme", "light")
    last_visit = request.COOKIES.get("last_time")
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_profile":
            new_name = request.POST.get("username", "").strip()
            selected_theme = request.POST.get("theme", "light")

            if new_name:
                request.session["username"] = new_name
            request.session["theme"] = selected_theme

            return redirect("home")

    response = render(
        request,
        "myprofile/index.html",
        {
            "username": username,
            "theme": theme,
            "last_visit": last_visit,
        },
    )
    response.set_cookie("last_time", current_time, max_age=60 * 60 * 24 * 30)
    return response


def tasks_view(request):
    tasks = request.session.get("tasks", [])
    theme = request.session.get("theme", "light")
    username = request.session.get("username", "Гість")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_task":
            task_name = request.POST.get("task", "").strip()
            if task_name:
                tasks.append(task_name)
                request.session["tasks"] = tasks
            return redirect("tasks")

        elif action == "remove_task":
            index = int(request.POST.get("index", "-1"))
            if 0 <= index < len(tasks):
                tasks.pop(index)
                request.session["tasks"] = tasks
            return redirect("tasks")

    return render(
        request,
        "myprofile/tasks.html",
        {
            "tasks": tasks,
            "theme": theme,
            "username": username,
            "total_tasks": len(tasks),
        },
    )


def settings_view(request):
    username = request.session.get("username", "Гість")
    theme = request.session.get("theme", "light")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "change_theme":
            new_theme = request.POST.get("theme", "light")
            request.session["theme"] = new_theme

        elif action == "clear_name":
            if "username" in request.session:
                del request.session["username"]
        elif action == "clear_tasks":
            request.session["tasks"] = []

        response = redirect("settings")
        if action == "delete_cookie":
            response.delete_cookie("last_time")

        return response

    return render(
        request,
        "myprofile/settings.html",
        {
            "username": username,
            "theme": theme,
        },
    )
