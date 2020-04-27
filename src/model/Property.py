class Property:

    def __init__(self, property_id, property_name):
        self.property_id = property_id
        self.property_name = property_name
        self.views = []

    def insert_view(self, View):
        self.views.append(View)

    def get_views(self):
        return self.views

    def get_property_id(self):
        return self.property_id

    def get_property_name(self):
        return self.property_name
