
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store tasks in memory
tasks = []
next_id = 1


@app.route("/")
def home():
    selected_filter = request.args.get("filter", "all")

    if selected_filter == "pending":
        visible_tasks = [t for t in tasks if not t["completed"]]
    elif selected_filter == "completed":
        visible_tasks = [t for t in tasks if t["completed"]]
    else:
        visible_tasks = tasks

    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed

    return render_template(
        "index.html",
        tasks=visible_tasks,
        current_filter=selected_filter,
        total=total,
        completed=completed,
        pending=pending
    )


@app.route("/tasks/add", methods=["POST"])
def add_task():
    global next_id

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "description": description,
            "completed": False
        })
        next_id += 1

    return redirect(url_for("home"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

    return redirect(url_for("home"))


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return "Task not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if title:
            task["title"] = title
            task["description"] = description
            return redirect(url_for("home"))

    return render_template("edit.html", task=task)



@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    tasks[:] = [t for t in tasks if t["id"] != task_id]

    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
