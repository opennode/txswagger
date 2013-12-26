import unittest

from swagger.core import ApiListingReference, ResourceListing


class ModelTestCaseMixin(object):
    model_class = None
    optional_parameters = ()

    @property
    def mandatory_parameters(self):
        return tuple(
            p for p in self.create_default_parameters().keys()
            if p not in self.optional_parameters
        )

    def test_mandatory_parameters_cannot_be_omitted(self):
        for mandatory_parameter in self.mandatory_parameters:
            # self.assertRaises doesn't fit here
            # since it doesn't provide means to customize failure message
            try:
                p1 = self.create_parameters(without=mandatory_parameter)
                self.model_class(**p1)
            except TypeError:
                pass
            else:
                self.fail('Was able to omit mandatory parameter "%s"' %
                          mandatory_parameter)

            try:
                kwargs = {mandatory_parameter: None}
                p2 = self.create_parameters(**kwargs)
                self.model_class(**p2)
            except TypeError:
                pass
            else:
                self.fail('Was able to set mandatory parameter "%s" to None' %
                          mandatory_parameter)

    def test_optional_parameters_can_be_omitted(self):
        for optional_parameter in self.optional_parameters:
            try:
                p1 = self.create_parameters(without=optional_parameter)
                self.model_class(**p1)
            except TypeError:
                self.fail('Unable to omit optional parameter "%s"' %
                          optional_parameter)

            try:
                kwargs = {optional_parameter: None}
                p2 = self.create_parameters(**kwargs)
                self.model_class(**p2)
            except TypeError:
                self.fail('Unable to set optional parameter "%s" to None' %
                          optional_parameter)

    def test_missing_optional_parameters_are_not_in_dict_representation(self):
        for parameter in self.optional_parameters:
            params = self.create_parameters(without=parameter)

            ref_dict = self.model_class(**params).as_dict()

            self.assertNotIn(parameter, ref_dict)

    def check_for_bad_values(self, argument_name, expected_type, bad_values):
        expected_message = ('Inappropriate argument type for "%s"; '
                            '%s expected' % (argument_name, expected_type))

        for value in bad_values:
            try:
                kwargs = {argument_name: value}
                self.model_class(**self.create_parameters(**kwargs))
            except TypeError as e:
                self.assertEqual(expected_message, e.message)
            else:
                self.fail('No type check was performed for parameter "%s"' %
                          argument_name)

    def create_default_parameters(self):
        raise NotImplementedError

    def create_parameters(self, **kwargs):
        without = kwargs.pop('without', ())
        if isinstance(without, str):
            without = (without,)

        p = self.create_default_parameters()
        p.update(kwargs)

        for parameter in without:
            try:
                del p[parameter]
            except KeyError:
                pass

        return p


class ApiListingReferenceTest(unittest.TestCase, ModelTestCaseMixin):
    model_class = ApiListingReference
    optional_parameters = ('description',)

    def test_path_must_be_string(self):
        self.check_for_bad_values('path', 'str',
                                  bad_values=(123, [], (), 12.34))

    def test_description_must_be_string(self):
        self.check_for_bad_values('description', 'str',
                                  bad_values=(123, [], (), 12.34))

    def create_default_parameters(self):
        return {
            'path': 'path',
            'description': 'description'
        }


class ResourceListingTest(unittest.TestCase, ModelTestCaseMixin):
    model_class = ResourceListing
    optional_parameters = ('description', 'info')

    def test_api_version_must_be_string(self):
        self.check_for_bad_values('api_version', 'str',
                                  bad_values=(123, [], (), 12.34))

    def test_description_must_be_string(self):
        self.check_for_bad_values('description', 'str',
                                  bad_values=(123, [], (), 12.34))

    def test_bad_apis_argument(self):
        api_ref = ApiListingReference('path1', 'descr1')
        bad_api_ref = 123

        self.check_for_bad_values('apis', 'iterable of ApiListingReference',
                                  bad_values=(
                                      'bad api ref',
                                      bad_api_ref,
                                      [api_ref, 'bad api ref'],
                                      (bad_api_ref, api_ref),
                                  ))

    def test_apis_turn_to_tuple_of_api_listing_references(self):
        api_ref1 = ApiListingReference('path1', 'descr1')
        api_ref2 = ApiListingReference('path2', 'descr2')

        expected_apis = (api_ref1, api_ref2)

        apis_parameters = (
            (api_ref1, api_ref2),
            [api_ref1, api_ref2],
            iter([api_ref1, api_ref2]),
            (api for api in expected_apis),
        )

        for apis_parameter in apis_parameters:
            params = self.create_parameters(apis=apis_parameter)
            listing = ResourceListing(**params)

            self.assertEqual(expected_apis, listing.apis)

    def create_default_parameters(self):
        return {
            'api_version': '0.1',
            'apis': (),
            'authorizations': (),
            'description': None,
            'info': None
        }
