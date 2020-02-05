from .base_form import NimaBaseForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(NimaBaseForm):
	busca = StringField('Busca', validators=[DataRequired()])
	artigos = BooleanField(validators=[])
	livros = BooleanField(validators=[])
	teses = BooleanField(validators=[])
	capitulos = BooleanField(validators=[])
	submit_id = SubmitField('Buscar')