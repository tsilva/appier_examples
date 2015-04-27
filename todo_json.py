import time
import appier
import calendar
import datetime
import appier_extras

class Todo(appier_extras.admin.Base):

    create_date = appier.field(type = float)
    name = appier.field()
    checked = appier.field(type = bool)

    def pre_save(self):
        self.create_date = time.time()

    def check_s(self):
        self.checked = True
        self.save()

    def uncheck_s(self):
        self.checked = False
        self.save()

class TodoApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self, 
            parts = (appier_extras.AdminPart,)
        )

    @appier.route("/todos.json")
    def list_todos_json(self):
        todos = Todo.find(map = True)
        for todo in todos: 
            action = "uncheck" if todo["checked"] else "check"
            todo["_%s_url" % action] = self.url_for("todo.%s_json" % action, id = todo["id"], absolute = True)
            todo["_delete_url"] = self.url_for("todo.delete_json", id = todo["id"], absolute = True)
        return todos

    @appier.route("/todos/new.json")
    def new_todo_json(self):
        todo = Todo.new()
        todo.name = self.field("name")
        todo.save()
        return self.redirect(self.url_for("todo.list_todos_json"))

    @appier.route("/todos/<int:id>/check.json")
    def check_json(self, id):
        todo = Todo.get(id = id).check_s()
        return self.redirect(self.url_for("todo.list_todos_json"))

    @appier.route("/todos/<int:id>/uncheck.json")
    def uncheck_json(self, id):
        todo = Todo.get(id = id).uncheck_s()
        return self.redirect(self.url_for("todo.list_todos_json"))

    @appier.route("/todos/<int:id>/delete.json")
    def delete_json(self, id):
        Todo.get(id = id).delete()
        return self.redirect(self.url_for("todo.list_todos_json"))

TodoApp().serve()
