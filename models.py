from app import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	return_code = db.Column(db.Integer)
	file_to_convert = db.Column(db.String())
	output1 = db.Column(db.String)
	output2 = db.Column(db.String)

	def __init__(self, return_code, file_to_convert, output1, output2):
		self.return_code = return_code
		self.file_to_convert = file_to_convert
		self.output1 = output1
		self.output2 = output2

	def __repr__(self):
		return '<id {}>'.format(self.id)