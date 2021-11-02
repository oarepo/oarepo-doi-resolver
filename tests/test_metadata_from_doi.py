
import json
from collections import namedtuple

from invenio_accounts.models import Role, User

TestUsers = namedtuple('TestUsers', ['u1', 'u2', 'u3', 'r1', 'r2'])

def test_response(app, db, client):
    """Returns named tuple (u1, u2, u3, r1, r2)."""
    with db.session.begin_nested():
        r1 = Role(name='role1')
        r2 = Role(name='role2')

        u1 = User(id=1, email='1@test.com', active=True, roles=[r1])
        u2 = User(id=2, email='2@test.com', active=True, roles=[r1, r2])
        u3 = User(id=3, email='3@test.com', active=True, roles=[r2])

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)

        db.session.add(r1)
        db.session.add(r2)

    response = client.get('/resolve-doi/10.5281/zenodo.5335900', content_type='application/json') #unauthorized user
    assert response.status_code == 401

    url = "https://localhost:5000/test/login/1"
    response = client.get(url)
    assert response.status_code == 200

    response = client.get('/resolve-article/10.5281/zenodo.5335900', content_type='application/json')  # authorized user
    assert response.status_code == 200

    response = client.get('/resolve-doi/xx/xx', content_type='application/json') #not existing DOI
    assert response.status_code == 404
