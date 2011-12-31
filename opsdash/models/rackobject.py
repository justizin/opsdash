import ptah
import sqlalchemy as sqla
from pyramid.httpexceptions import HTTPNotFound

class RackObject(ptah.cms.Node):
    """ A basic model. """
    
    __tablename__ = 'rackptahbles_object'
   
    # Required primary field
    __id__ = sqla.Column('id', sqla.Integer,
                         sqla.ForeignKey('ptah_nodes.id'),
                         primary_key=True)

    # Your custom fields
    title = sqla.Column(sqla.Unicode)
    label = sqla.Column(sqla.Unicode)
    objtype = sqla.Column(sqla.Integer)
    asset_no = sqla.Column(sqla.Unicode)
    has_problems = sqla.Column(sqla.Boolean)
    comment = sqla.Column(sqla.Unicode)

    # Declare it as a Ptah Model
    __type__ = ptah.cms.Type('RackObject')

def factory(request):
    id_ = request.matchdict.get('id')
    if id_:
        return ptah.cms.Session.query(RackObject) \
               .filter(RackObject.__id__ == id_).first()

    return HTTPNotFound(location='.')
