from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Button_WelcomeUser(FlaskForm):
    start = SubmitField('Iniciar')


class Button_DatabaseSync(FlaskForm):
    dbsync = SubmitField('Sincronizar com DB MySQL')


# TODO: Funcionalidade não implementada
# Disponibilizar um formulário para o usuário configurar os parâmetros
# de conexão com o DB
class Form_DatabaseSync(FlaskForm):
    hostname = StringField('Host')
    username = StringField('User')
    password = PasswordField('Password')
    start = SubmitField('Iniciar')


# TODO: Funcionalidade não implementada
# Inserir um novo registro de usuário no DB e
# posteriormente inserir no Google Analytics
class Form_InsertUser(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired()])
    permission_edit = BooleanField('Editar')
    permission_manage_users = BooleanField('Gerenciar usuários')
    permission_collaborate = BooleanField('Colaborar')
    permission_read_and_analyze = BooleanField('Ler e analisar')
    submit = SubmitField('Inserir')
