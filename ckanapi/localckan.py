from ckanapi.errors import CKANAPIError
from ckanapi.common import ActionShortcut

class LocalCKAN(object):
    """
    An interface to calling actions with get_action() for CKAN plugins.

    :param username: perform action as this user, defaults to the site user
                     and stored as self.username
    :param context: a default context dict to use when calling actions,
                    stored as self.context with username added as its 'user'
                    value
    """
    def __init__(self, username=None, context=None):
        from ckan.logic import get_action
        self._get_action = get_action

        if not username:
            username = self.get_site_username()
        self.username = username
        self.context = dict(context or [], user=self.username)
        self.action = ActionShortcut(self)

    def get_site_username(self):
        user = self._get_action('get_site_user')({'ignore_auth': True}, ())
        return user['name']

    def call_action(self, action, data_dict=None, context=None, apikey=None):
        """
        :param action: the action name, e.g. 'package_create'
        :param data_dict: the dict to pass to the action, defaults to {}
        :param context: an override for the context to use for this action,
                        remember to include a 'user' when necessary
        """
        if not data_dict:
            data_dict = []
        if context is None:
            context = self.context
        if apikey:
            # FIXME: allow use of apikey to set a user in context?
            raise CKANAPIError("LocalCKAN.call_action does not support "
                "use of apikey parameter, use context['user'] instead")
        # copy dicts because actions may modify the dicts they are passed
        return self._get_action(action)(dict(context), dict(data_dict))
