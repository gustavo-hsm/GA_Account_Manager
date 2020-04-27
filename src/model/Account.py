class Account:

    def __init__(self, account_id, account_name):
        self.account_id = account_id
        self.account_name = account_name
        self.web_properties = []

    def insert_web_property(self, Property):
        self.web_properties.append(Property)

    def get_web_properties(self):
        return self.web_properties

    def get_account_id(self):
        return self.account_id

    def get_account_name(self):
        return self.account_name
