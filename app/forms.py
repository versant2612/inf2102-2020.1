from .base_form import NimaBaseForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(NimaBaseForm):
	busca = StringField('Busca', validators=[DataRequired()])
	submit_id = SubmitField('Buscar')