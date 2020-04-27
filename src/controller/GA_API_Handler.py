"""
GA API Handler

Módulo implementado para gerenciar conexões com o Google Analytics
por intermédio de uma conta de serviço

# Modo de utilização
Utilizar o método 'get_instance()' para convocar uma instância única
da classe GA_API_Handler, fornecendo via parâmetro o diretório contendo
o arquivo "client_secret" da Service Account. Um token de acesso temporário
será disponibilizado para efetuar operações na API do Google Analytics.

A partir desta instância, utilizar as funções 'query_account_summary'
e 'query_all_users' para buscar informações pertinentes a contas
e usuários, respectivamente.
"""
from os import walk
from functools import reduce

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from ..model import Account as acc
from ..model import Property as pro
from ..model import View as viw
from ..model import User as usr


class GA_API_Handler:
    instance = None

    class __GA_API_Handler:
        def __init__(self, dir_secrets, auth_method):
            self.api = 'analytics'
            self.api_version = 'v3'
            self.scopes = [
                'https://www.googleapis.com/auth/analytics.readonly',
                'https://www.googleapis.com/auth/analytics.edit',
                'https://www.googleapis.com/auth/analytics.manage.users',
                'https://www.googleapis.com/auth/analytics.manage.users.\
                    readonly']
            # Carregando secrets.JSON
            self.secrets = self._find_secrets(dir_secrets)

            # Carregando credenciais
            self.credentials = self._service_account_credentials()

            # Construindo um token de acesso
            self.service = self._build_service_token()

        def _find_secrets(self, dir_secrets):
            secrets = []
            for root, dirs, files in walk(dir_secrets):
                for file in files:
                    if file.endswith('.json'):
                        secret = root + '/' + file
                        secrets.append(secret)
            if len(secrets) < 1:
                raise FileNotFoundError('Nenhum arquivo .json encontrado no \
                    diretório "%s"' % dir_secrets)

            return secrets

        def _service_account_credentials(self):
            # TODO: Carregar credenciais para múltiplos 'client secrets'
            return ServiceAccountCredentials.from_json_keyfile_name(
                self.secrets[0], scopes=self.scopes)

        def _build_service_token(self):
            try:
                return build(self.api,
                             self.api_version,
                             credentials=self.credentials)

            except HttpError:
                self._alert_http_error(HttpError)

        def _alert_http_error(self, error):
            print('Ocorreu um erro durante a tentativa de acessar a API:\
                %s %s' % (self.api, self.api_version))
            print('%s (%s)' % (error.resp.status, error.resp.reason))

        def _request_account_summary(self):
            try:
                response = self.service.management().accountSummaries()\
                    .list().execute()
                self._log_api_request(response)
                return(response)
            except HttpError:
                self._alert_http_error(HttpError)

        def _request_user_links(self, account_id):
            try:
                response = self.service.management().accountUserLinks()\
                    .list(accountId=account_id).execute()
                self._log_api_request(response)
                return(response)
            except HttpError:
                self._alert_http_error(HttpError)

        # TODO: Função não implementada
        # Registrar logs com todas chamadas de API
        def _log_api_request(self, response):
            pass

        def query_account_summary(self):
            request = self._request_account_summary()
            accounts = []

            for acc_data in request['items']:
                account = acc.Account(acc_data['id'], acc_data['name'])
                for prop_data in acc_data['webProperties']:
                    prop = pro.Property(prop_data['id'], prop_data['name'])
                    for view_data in prop_data['profiles']:
                        view = viw.View(view_data['id'], view_data['name'])
                        prop.insert_view(view)
                    account.insert_web_property(prop)
                accounts.append(account)

            return accounts

        def query_users_by_account(self, account_id):
            request = self._request_user_links(account_id)
            users = []

            for item in request['items']:
                user = usr\
                    .User(user_id=item['userRef']['id'],
                          user_account_id=item['entity']['accountRef']['id'],
                          user_email=item['userRef']['email'],
                          user_local_permission=item['permissions']
                                                    ['local'],
                          user_global_permission=item['permissions']
                                                     ['effective'])
                users.append(user)

            return users

        def query_all_users(self, accounts):
            account_ids = set([x.get_account_id() for x in accounts])
            users = [self.query_users_by_account(x) for x in account_ids]

            return reduce(lambda x, y: x + y, users)

    def __init__(self, dir_secrets='service_account_secrets',
                 auth_method='service_account'):
        if not GA_API_Handler.instance:
            self.instance = GA_API_Handler\
                .__GA_API_Handler(dir_secrets, auth_method)

    def get_instance(self):
        return self.instance
