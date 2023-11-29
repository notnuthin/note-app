from app import app_obj, db
from app.models import User, Note
@app_obj.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Note': Note}
app_obj.run(debug=True, port=5002)
