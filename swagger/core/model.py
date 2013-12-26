from collections import namedtuple


# Overriding __init__ in the following classes is not sufficient
# due to the way namedtuple is implemented.

class ApiListingReference(namedtuple('_ApiListingReference',
                                     'path description')):
    def __new__(cls, path, description=None):
        if not isinstance(path, str):
            raise TypeError(
                'Inappropriate argument type for path; str expected')

        if description is not None and not isinstance(description, str):
            raise TypeError(
                'Inappropriate argument type for description; str expected')

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

    def __new__(cls, api_version, apis=(), authorizations=(),
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
        if authorizations:
            raise NotImplementedError('authorizations are not supported yet')

        if info is not None:
            raise NotImplementedError('info is not supported yet')

        if isinstance(apis, str):
            raise TypeError('Inappropriate argument type for apis. '
                            'Iterable of ApiListingReference expected.')

        def ensure_api(api):
            if not isinstance(api, ApiListingReference):
                raise TypeError('Inappropriate argument type for apis. '
                                'Iterable of ApiListingReference expected.')
            return api

        try:
            api_iterator = iter(apis)
        except TypeError:
            raise TypeError('Inappropriate argument type for apis. '
                            'Iterable of ApiListingReference expected.')

        apis = tuple(ensure_api(api) for api in api_iterator)

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
