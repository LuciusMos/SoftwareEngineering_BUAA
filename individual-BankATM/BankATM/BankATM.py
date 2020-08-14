from app import application, database
from app.models import User, Operation


@application.shell_context_processor
def make_shell_context():
    return {'database': database, 'User': User, 'Operation': Operation}


# app.run(debug=True)
application.run(host='0.0.0.0')
