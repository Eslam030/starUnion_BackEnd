class mainRouter:
    route_app_labels = {"auth", "main", "admin", "contenttypes",
                        "sessions", "messages", "staticfiles"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "main_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "main_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels and db == "main_db":
            return True
        else:
            return None


class workShopRouter:
    route_app_labels = {"workshops", "main"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "workshops_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "workshops_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels and db == "workshops_db":
            return True
        else:
            return None


class eventRouter:
    route_app_labels = {"events", "main"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "events_db"
        return False

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "events_db"
        return False

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels and db == "events_db":
            return True
        else:
            return False
