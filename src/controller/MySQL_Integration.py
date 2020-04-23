""" 
MySQL Integration

Classe de apoio para implementar a conexão entre o
cliente e o Database.

# Pré-requisitos
	* É necessário que exista um SGBD MySQL instalado
	no local de utilização deste aplicativo.

	* Os scripts disponibilizados em 'start_db.sql'
	devem ser executados para inicializar a estrutura
	básica do Database

# Modo de utilização
	Criar uma instância da classe MySQL_DB(), preenchendo
	os parâmetros com as credenciais de acesso necessárias.
	A conexão com o Database será realizada durante a
	execução do construtor.

	Após a criação da classe, os métodos 'insert_account' e
	'insert_user' podem ser utilizados para sincronizar os
	dados obtidos pela API Google Analytics com o Database.
"""

from datetime import datetime

import mysql.connector as msql


class MySQL_DB:
	

	def __init__(self, host='localhost', user='root', pwd='', 
		db_name='GA_Account_Summary'):
		self.db_name = db_name
		self.host = host
		self.user = user
		self.pwd = pwd

		try:
			self.db_connection = msql.connect(
				host = self.host, user = self.user,
				passwd = self.pwd, database = self.db_name
			)
		except msql.errors.ProgrammingError as error:
			self._alert_transaction_error(error)

	def _query_account_id(self, id_analytics):
		query = 'SELECT id FROM Account WHERE id_analytics = "%s"' % id_analytics
		return self._execute_query(query, fetch=True)

	def _query_property_id(self, id_analytics):
		query = 'SELECT id FROM Property WHERE id_analytics = "%s"' % id_analytics
		return self._execute_query(query, fetch=True)

	def _insert_property(self, Property, id_account):
		fk_id_account = self._query_account_id(id_account)[0][0]
		query = 'INSERT INTO Property(id_analytics, id_account, txt_property_name) VALUES ("%s", "%s", "%s")' % (
			Property.get_property_id(),
			fk_id_account,
			Property.get_property_name()
		)
		self._execute_query(query)
		for view in Property.get_views():
			self._insert_view(view, Property.get_property_id())

	def _insert_view(self, View, id_property):
		fk_id_property = self._query_property_id(id_property)[0][0]
		query = 'INSERT INTO View(id_analytics, id_property, txt_view_name) VALUES ("%s", "%s", "%s")' % (
			View.get_view_id(),
			fk_id_property,
			View.get_view_name()
		)
		self._execute_query(query)

	def _alert_transaction_error(self, error):
		print('Erro durante a comunicação com o database "%s"' % self.host)
		print('"%s" - "%s"' % (error.errno, error.msg))

	def _execute_query(self, query, fetch=False):
		cursor = self.db_connection.cursor()

		try:
			cursor.execute(query),
			if fetch:
				return cursor.fetchall()
			else:
				self.db_connection.commit()
				self._log_transaction()
		except msql.errors.ProgrammingError as error:
			self._alert_transaction_error(error)
			self.db_connection.rollback()
		except msql.errors.IntegrityError as error:
			if error.errno == 1062:
				print('Tentativa de inserir um registro duplicado: "%s¨' % query)
				self.db_connection.rollback()
				pass
		finally:
			cursor.close()

	#TODO: Recurso não implementado
	def _log_transaction(self):
		pass

	def insert_account(self, Account):
		query = 'INSERT INTO Account(id_analytics, txt_account_name) VALUES ("%s", "%s")' % (
			Account.get_account_id(),
			Account.get_account_name()
		)
		self._execute_query(query)
		for prop in Account.get_web_properties():
			self._insert_property(prop, Account.get_account_id())
			
	def insert_user(self, User):
		id_account = self._query_account_id(User.get_user_account_id())[0][0]
		query = 'INSERT INTO User (id_analytics, id_account, txt_user_email, txt_user_local_permission, txt_user_global_permission) VALUES ("%s", "%s", "%s", "%s", "%s")' % (
			User.get_user_id(),
			id_account,
			User.get_user_email(),
			', '.join(User.get_user_local_permission()),
			', '.join(User.get_user_global_permission())
		)
		self._execute_query(query)
