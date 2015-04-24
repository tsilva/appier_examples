import appier
import calendar
import datetime
import appier_extras

class Todo(appier_extras.admin.Base):

    create_date = appier.field(
        type = float
    )

    name = appier.field()

    checked = appier.field(
        type = bool
    )

    def pre_save(self):
        self.create_date = self.now()

    def pre_create(self):
        self.checked = False

    def check_s(self):
        self.checked = True
        self.save()

    def uncheck_s(self):
        self.checked = False
        self.save()

    def now(self):
        date = datetime.datetime.utcnow()
        date_utc = date.utctimetuple()
        timestamp = calendar.timegm(date_utc)
        return timestamp

class TodoApp(appier.WebApp):

    BASE_URL = "http://localhost:8080"

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
            todo["_%s_url" % action] = self.BASE_URL + self.url_for("todo.%s_json" % action, id = todo["id"])
            todo["_delete_url"] = self.BASE_URL + self.url_for("todo.delete_json", id = todo["id"])
        return todos

    @appier.route("/todos/new.json")
    def new_todo_json(self):
        todo = Todo.new()
        todo.name = self.get_field("name")
        todo.save()
        return self.redirect(
            self.url_for("todo.list_todos_json")
        )

    @appier.route("/todos/<int:id>/check.json")
    def check_json(self, id):
        todo = Todo.get(id = id)
        todo.check_s()
        return self.redirect(
            self.url_for("todo.list_todos_json")
        )

    @appier.route("/todos/<int:id>/uncheck.json")
    def uncheck_json(self, id):
        todo = Todo.get(id = id)
        todo.uncheck_s()
        return self.redirect(
            self.url_for("todo.list_todos_json")
        )

    @appier.route("/todos/<int:id>/delete.json")
    def delete_json(self, id):
        todo = Todo.get(id = id)
        todo.delete()
        return self.redirect(
            self.url_for("todo.list_todos_json")
        )

TodoApp().serve()
