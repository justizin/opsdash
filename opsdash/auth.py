import ptah
import sqlalchemy as sqla

@ptah.auth_provider('custom-user')
class AuthProvider(object):

    def authenticate(self, creds):
        login, password = creds['login'], creds['password']

        user = User.get_bylogin(login)

        if user is not None:
            if ptah.pwd_tool.check(user.password, password):
                return user

    def get_principal_bylogin(self, login):
        return User.get_bylogin(login)


class User(ptah.get_base()):

    __tablename__ = 'rackptahbles_users'

    pid = sqla.Column(sqla.Integer, primary_key=True)
    uri = sqla.Column(sqla.Unicode, unique=True, info={'uri': True})
    name = sqla.Column(sqla.Unicode)
    login = sqla.Column(sqla.Unicode, unique=True)
    email = sqla.Column(sqla.Unicode, unique=True)
    password = sqla.Column(sqla.Unicode)
    _uri_gen = ptah.UriFactory('custom-user')

    def __init__(self, name, login, email, password=u''):
        super(User, self).__init__()

        self.name = name
        self.login = login
        self.email = email
        self.password = ptah.pwd_tool.encode(password)
        self.uri = self._uri_gen()

    @classmethod
    def get_byuri(cls, uri):
        return ptah.get_session().query(User).filter(User.uri==uri).first()

    @classmethod
    def get_bylogin(cls, login):
        return ptah.get_session().query(User).filter(User.login==login).first()


@ptah.principal_searcher('custom-user')
def search(term):
    term = '%%%s%%'%term

    q = ptah.get_session().query(CrowdUser) \
        .filter(sqla.sql.or_(CrowdUser.email.contains(term),
                             CrowdUser.name.contains(term)))\
                             .order_by(sqla.sql.asc('name'))
    for user in q:
        yield user


@ptah.resolver('custom-user')
def get_byuri(uri):
    """User resolver"""
    return User.get_byuri(uri)


@ptah.password_changer('custom-user')
def change_pwd(principal, password):
    principal.password = password
