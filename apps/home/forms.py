# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present trustle.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired

# User Name Generator


class UserNameGeneratorForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])
class CreatePatternFrom(FlaskForm):
    pattern     =   StringField('Pattern',
                         id='id_pattern',
                         validators=[DataRequired()])
    type        =   IntegerField('Type',
                         id='id_type',
                         validators=[DataRequired()])
    Rank        =   IntegerField('Rank',
                             id='id_rank',
                             validators=[DataRequired()])
    description =   StringField('Description',
                         id='id_description',
                         validators=[DataRequired()])

