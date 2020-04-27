class User:

    def __init__(self,
                 user_id, user_account_id, user_email,
                 user_local_permission,
                 user_global_permission):
        self.user_id = user_id
        self.user_account_id = user_account_id
        self.user_email = user_email
        self.user_local_permission = user_local_permission
        self.user_global_permission = user_global_permission

    def get_user_id(self):
        return self.user_id

    def get_user_account_id(self):
        return self.user_account_id

    def get_user_email(self):
        return self.user_email

    def get_user_local_permission(self):
        return self.user_local_permission

    def get_user_global_permission(self):
        return self.user_global_permission
