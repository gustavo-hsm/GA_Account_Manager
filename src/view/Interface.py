from . import User_Forms as forms
from ..controller import GA_API_Handler as ga
from ..controller import Interface_Handler as ih
from ..controller import MySQL_Integration as msql

from flask import render_template
from flask import request

def render_welcome():
    return render_template('welcome.html',
        title='Home',
        form=forms.Button_WelcomeUser())

def render_account_summary():
    #Construindo um token de acesso à API do Google Analytics
    api_handler = ga.GA_API_Handler().get_instance()

    #Buscando contas, propriedades e vistas
    api_accounts = api_handler.query_account_summary()

    #Buscando usuários
    api_users = api_handler.query_all_users(api_accounts)

    #Denormalizando dados para apresentação em página HTML
    accounts = ih.denormalize_accounts(api_accounts)
    users = ih.denormalize_users(api_users)

    return render_template('account_summary.html', 
        title='Summary', 
        account_list=accounts,
        user_list=users,
        form=forms.Button_DatabaseSync())

def render_db_sync():
    #Construindo um token de acesso à API do Google Analytics
    api_handler = ga.GA_API_Handler().get_instance()

    #Buscando contas, propriedades e vistas
    api_accounts = api_handler.query_account_summary()

    #Buscando usuários
    api_users = api_handler.query_all_users(api_accounts)

    for account in api_accounts:
        db.insert_account(account)

    for user in api_users:
        db.insert_user(user)
    
    return render_template('dbsync.html', title='MySQL DB')


def render_error_page(error_code):
    error_page = {
        404: ['error_page_404.html', '404 - Recurso não encontrado'],
        500: ['error_page_500.html', '500 - Erro de processamento']
    }.get(error_code)

    return render_template(error_page[0], title=error_page[1])