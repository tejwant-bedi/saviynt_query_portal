from datetime import datetime
from extensions import db

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    query_text = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)