from flask import redirect

from flask_security import login_required

from auth import auth


@auth.route('/auth/')
@login_required
def auth_index():
    return redirect('/admin/')

