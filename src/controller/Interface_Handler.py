""" 
Interface Handler

Funções de apoio para processamento dos dados
disponibilizados na View 'Interface'
"""

def denormalize_accounts(accounts: list):
    """ 
    Denormalize Accounts

    Dada uma lista de model.Accounts, denormalizar
    os atributos contidos na própria conta, 
    propriedades e vistas associadas.

    O resultado será uma lista redundante de registros, para
    apresentação da tabela 'contas, propriedades e vistas',
    no template 'src/view/templates/account_summary.html'
    """
    account_list = []

    for account in accounts:
        
        account_id = account.get_account_id()
        account_name = account.get_account_name()
        property_id = ''
        property_name = ''
        view_id = ''
        view_name = ''

        for prop in account.get_web_properties():
            property_id = prop.get_property_id()
            property_name = prop.get_property_name()

            for view in prop.get_views():
                view_id = view.get_view_id()
                view_name = view.get_view_name()

                account_list.append({
                    'account_id': account_id,
                    'account_name': account_name,
                    'property_id': property_id,
                    'property_name': property_name,
                    'view_id': view_id,
                    'view_name': view_name,
                })
    return account_list

def denormalize_users(users: list):
    """ 
    Denormalize Users

    Dada uma lista de Users, extrair as propriedades de cada
    usuário em uma lista de dicionários.

    O resultado será uma lista redundante de registros, para
    apresentação da tabela 'usuários' no template 
    'src/view/templates/account_summary.html'
    """
    user_list = []

    for user in users:

        user_id = user.get_user_id()
        user_account_id = user.get_user_account_id()
        user_email = user.get_user_email()
        user_local_permission = user.get_user_local_permission()
        user_global_permission = user.get_user_global_permission()

        user_list.append({
            'user_id': user_id,
            'user_account_id': user_account_id,
            'user_email': user_email,
            'user_local_permission': user_local_permission,
            'user_global_permission': user_global_permission,
        })

    return user_list
