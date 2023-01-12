import sys
import traceback

from flask_mde import MdeField
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField


class MdeForm(FlaskForm):
    editor = MdeField()
    submit = SubmitField('Save')


def error_printer(er):
    print('SQLite error: %s' % (' '.join(er.args)))
    print("Exception class is: ", er.__class__)
    print('SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
