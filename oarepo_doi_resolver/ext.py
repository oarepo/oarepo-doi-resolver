import requests
from crossref.restful import Works
from flask import Blueprint, abort
from invenio_base.signals import app_loaded
from simplejson import JSONDecodeError

from oarepo_doi_resolver.relatedItems_metadata_mapping import schema_mapping


class CrossRefClient(object):
    """Class for CrossRefClient."""

    def __init__(self, accept='text/x-bibliography; style=apa', timeout=3):
        """
        # Defaults to APA biblio style.

        # Usage:
        s = CrossRefClient()
        print s.doi2apa("10.1038/nature10414")
        """
        self.headers = {'accept': accept}
        self.timeout = timeout

    def query(self, doi, q={}):
        #Get query.
        if doi.startswith("http://"):
            url = doi
        else:
            url = "http://dx.doi.org/" + doi

        r = requests.get(url, headers=self.headers)
        return r

    def doi2apa(self, doi):
        self.headers['accept'] = 'text/x-bibliography; style=apa'
        return self.query(doi).text

    def doi2turtle(self, doi):
        self.headers['accept'] = 'text/turtle'
        return self.query(doi).text

    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

    def doi2xml(self, doi):
        self.headers['accept'] = 'application/rdf+xml'
        return self.query(doi).text

def getMetadataFromDOI(id):
    works = Works()
    metadata = works.doi(id)

    if metadata is None:
        s = CrossRefClient()
        metadata = s.doi2json(id)
    metadata.pop('id', None)
    return metadata

def resolve_doi(**kwargs):
    from flask_login import current_user
    if not current_user.is_authenticated:
        abort(401)
    first_part = kwargs['first_part']
    second_part = kwargs['second_part']
    doi = first_part + '/' + second_part

    try:
        metadata = getMetadataFromDOI(doi)
    except JSONDecodeError:
        abort(404)
    except:
        abort(500)

    return metadata

def resolve_article(**kwargs):
    from flask_login import current_user
    if not current_user.is_authenticated:
        abort(401)
    first_part = kwargs['first_part']
    second_part = kwargs['second_part']
    doi = first_part + '/' + second_part

    try:
        metadata = getMetadataFromDOI(doi)
    except JSONDecodeError:
        abort(404)
    except:
        abort(500)

    article = schema_mapping(metadata, doi)

    return article

def resolve_doi_ext(sender, app=None, **kwargs):
    with app.app_context():
        resolve_doi_bp = Blueprint("resolve_doi", __name__, url_prefix=None, )
        resolve_doi_bp.add_url_rule(rule='/resolve-doi/<string:first_part>/<string:second_part>', view_func=resolve_doi, methods=['GET'])
        app.register_blueprint(resolve_doi_bp)

        resolve_article_bp = Blueprint("resolve_article", __name__, url_prefix=None, )
        resolve_article_bp.add_url_rule(rule='/resolve-article/<string:first_part>/<string:second_part>', view_func=resolve_article,
                                    methods=['GET'])
        app.register_blueprint(resolve_article_bp)



class OARepoDOIResolver:
    def __init__(self, app=None, db=None):
        self.init_app(app, db)

    def init_app(self, app, db):
        app_loaded.connect(resolve_doi_ext)