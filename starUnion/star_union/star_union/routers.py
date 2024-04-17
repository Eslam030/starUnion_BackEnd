# why did i cancel using multiple databases for different apps ??
# the connection between the databases is not working properly
# so if i want to do this i will have to implement a custom admin forms
# why ??
# because the relations will be made using only the id of the instance
# so to view the related instances i will have to make a custom admin form
# so i need to read more in django jazzmin template
# to now how it is implemented
# i will leave this for now
# in the up comming delivery i will implement this
# for now we are using one database (main_db)
class mainRouter:
    route_app_labels = {"auth", "main", "admin", "contenttypes",
                        "sessions", "messages", "staticfiles", 'events', 'workshops'}
    route_app_labels2 = {}
    route_app_labels3 = {}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "main_db"
        if model._meta.app_label in self.route_app_labels2:
            return "events_db"
        elif model._meta.app_label in self.route_app_labels3:
            return "workshops_db"
        return False

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return "main_db"
        if model._meta.app_label in self.route_app_labels2:
            return "events_db"
        elif model._meta.app_label in self.route_app_labels3:
            return "workshops_db"
        return False

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj1._meta.app_label in self.route_app_labels2
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels and db == "main_db":
            return True
        elif app_label in self.route_app_labels2 and db == "events_db":
            return True
        elif app_label in self.route_app_labels3 and db == "workshops_db":
            return True
        else:
            return False
