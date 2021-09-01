# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import os
import shutil
import sys

import flask
import invenio_records_rest
import pytest
from flask import Flask, current_app, make_response, url_for
from flask_login import LoginManager, login_user
from flask_principal import Identity, Principal, identity_changed
from invenio_access import InvenioAccess, authenticated_user
from invenio_access.permissions import Permission
from invenio_accounts.models import Role, User
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_db import db as _db
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.utils import PIDConverter, allow_all
from invenio_records_rest.views import create_blueprint_from_app, need_record_permission
from invenio_rest import InvenioREST
from invenio_search import InvenioSearch
from invenio_search.cli import destroy, init
from oarepo_mapping_includes.ext import OARepoMappingIncludesExt
from oarepo_validate.ext import OARepoValidate
from sqlalchemy_utils import create_database, database_exists

from oarepo_actions.ext import Actions

from oarepo_doi_resolver import OARepoDOIResolver


def set_identity(u):
    """Sets identity in flask.g to the user."""
    identity = Identity(u.id)
    identity.provides.add(authenticated_user)
    identity_changed.send(current_app._get_current_object(), identity=identity)
    assert flask.g.identity.id == u.id

@pytest.fixture()
def base_app():
    """Flask applicat-ion fixture."""
    instance_path = os.path.join(sys.prefix, 'var', 'test-instance')

    # empty the instance path
    if os.path.exists(instance_path):
        shutil.rmtree(instance_path)
    os.makedirs(instance_path)

    os.environ['INVENIO_INSTANCE_PATH'] = instance_path

    app_ = Flask('invenio-model-testapp', instance_path=instance_path)
    app_.config.update(
        TESTING=True,
        JSON_AS_ASCII=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///:memory:'),
        SERVER_NAME='localhost:5000',
        SECURITY_PASSWORD_SALT='TEST_SECURITY_PASSWORD_SALT',
        SECRET_KEY='TEST_SECRET_KEY',
        INVENIO_INSTANCE_PATH=instance_path,
        SEARCH_INDEX_PREFIX='test-',
        JSONSCHEMAS_HOST='localhost:5000',
        SEARCH_ELASTIC_HOSTS=os.environ.get('SEARCH_ELASTIC_HOSTS', None),
        PIDSTORE_RECID_FIELD='InvenioID',
        FILES_REST_PERMISSION_FACTORY = allow_all
    )

    InvenioDB(app_)
    InvenioIndexer(app_)
    InvenioSearch(app_)

    return app_


@pytest.yield_fixture()
def app(base_app):
    """Flask application fixture."""

    base_app._internal_jsonschemas = InvenioJSONSchemas(base_app)

    InvenioREST(base_app)
    InvenioRecordsREST(base_app)

    InvenioRecords(base_app)
    InvenioPIDStore(base_app)
    base_app.url_map.converters['pid'] = PIDConverter
    OARepoDOIResolver(base_app)
    OARepoMappingIncludesExt(base_app)
    LoginManager(base_app)
    Permission(base_app)
    InvenioAccess(base_app)
    Principal(base_app)
    OARepoValidate(base_app)
    Actions(base_app)
    base_app.register_blueprint(invenio_records_rest.views.create_blueprint_from_app(base_app))
    login_manager = LoginManager()
    login_manager.init_app(base_app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def basic_user_loader(user_id):
        user_obj = User.query.get(int(user_id))
        return user_obj

    @base_app.route('/test/login/<int:id>', methods=['GET', 'POST'])
    def test_login(id):
        print("test: logging user with id", id)
        response = make_response()
        user = User.query.get(id)
        login_user(user)
        set_identity(user)
        return response

    app_loaded.send(None, app=base_app)

    with base_app.app_context():
        yield base_app




@pytest.yield_fixture()
def client(app):
    """Get test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    """Create database for the tests."""
    with app.app_context():
        if not database_exists(str(_db.engine.url)) and \
                app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite://':
            create_database(_db.engine.url)
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


# @pytest.fixture()
# def prepare_es(app, db):
#     runner = app.test_cli_runner()
#     result = runner.invoke(destroy, ['--yes-i-know', '--force'])
#     if result.exit_code:
#         print(result.output, file=sys.stderr)
#     assert result.exit_code == 0
#     result = runner.invoke(init)
#     if result.exit_code:
#         print(result.output, file=sys.stderr)
#     assert result.exit_code == 0