from collections import namedtuple


def _arg_wront_type_msg(parameter, expected_type='str'):
    return ('Inappropriate argument type for "%s"; %s expected' %
            (parameter, expected_type))


# Overriding __init__ in the following classes is not sufficient
# due to the way namedtuple is implemented.

class ApiListingReference(namedtuple('_ApiListingReference',
                                     'path description')):
    def __new__(cls, path, description=None):
        if not isinstance(path, str):
            raise TypeError(_arg_wront_type_msg('path'))

        if description is not None and not isinstance(description, str):
            raise TypeError(_arg_wront_type_msg('description'))

        return super(ApiListingReference, cls).__new__(cls, path, description)

    def as_dict(self):
        """
        Returns own representation as a dictionary.

        Missing optional fields are not in the dictionary.

        :rtype dict:
        """
        result = self._asdict()

        if self.description is None:
            del result['description']

        return result


class ResourceListing(
    namedtuple('_ResourceListing',
               'api_version apis authorizations description info')):
    """
    Represents an inventory of all the APIs provided by the service.

    see https://github.com/wordnik/swagger-core/wiki/Resource-Listing
    """

    def __new__(cls, api_version, apis, authorizations,
                description=None, info=None):
        """
        :param api_version: Version of the API being described
        :type api_version: str
        :param apis: APIs to point to
        :type apis: iterable of ApiListingReference
        :param authorizations: Supported authorization types
        :type authorizations: iterable of AuthorizationType
        :param description: Optional description of what the API does
        :type description: str
        :param info: Optional information about the API authors and contacts
        :type info: str
        """
        if not isinstance(api_version, str):
            raise TypeError(_arg_wront_type_msg('api_version'))

        try:
            auth_iterator = iter(authorizations)
        except TypeError:
            raise TypeError(_arg_wront_type_msg(
                'authorizations', 'iterable of AuthorizationType'))

        authorizations = tuple(auth_iterator)
        if authorizations:
            raise NotImplementedError('"authorizations" are not supported yet')

        if info is not None:
            raise NotImplementedError('info is not supported yet')

        if isinstance(apis, str):
            raise TypeError(_arg_wront_type_msg(
                'apis', 'iterable of ApiListingReference'))

        def ensure_api(api):
            if not isinstance(api, ApiListingReference):
                raise TypeError(_arg_wront_type_msg(
                    'apis', 'iterable of ApiListingReference'))
            return api

        try:
            api_iterator = iter(apis)
        except TypeError:
            raise TypeError(_arg_wront_type_msg(
                'apis', 'iterable of ApiListingReference'))

        apis = tuple(ensure_api(api) for api in api_iterator)

        if description is not None and not isinstance(description, str):
            raise TypeError(_arg_wront_type_msg('description'))

        return super(ResourceListing, cls).__new__(cls, api_version, apis,
                                                   authorizations,
                                                   description, info)

    def as_dict(self):
        """
        Returns own representation as a dictionary.

        Missing optional fields are not in the dictionary.

        :rtype dict:
        """

        data = self._asdict()

        data["swaggerVersion"] = '1.2'

        if self.description is None:
            del data['description']

        if self.info is None:
            del data['info']

        return data

