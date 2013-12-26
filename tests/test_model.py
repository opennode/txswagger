import unittest

from swagger.core import ApiListingReference, ResourceListing


class ParameterProviderMixin(object):
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


class ApiListingReferenceTest(unittest.TestCase, ParameterProviderMixin):
    optional_parameters = ('description',)

    def test_description_is_optional(self):
        p1 = self.create_parameters(without='description')
        ApiListingReference(**p1)

        p2 = self.create_parameters(description=None)
        ApiListingReference(**p2)

    def test_description_must_be_string(self):
        expected_message = ('Inappropriate argument type for description; '
                            'str expected')

        bad_values = (123, [], (), 12.34)

        for value in bad_values:
            with self.assertRaises(TypeError) as m:
                ApiListingReference(**self.create_parameters(description=value))
            self.assertEqual(expected_message, m.exception.message)

    def test_path_is_mandatory(self):
        p = self.create_parameters(path=None)

        with self.assertRaises(TypeError):
            ApiListingReference(**p)

        p = self.create_parameters(without='description')
        del p['path']

        with self.assertRaises(TypeError):
            ApiListingReference(**p)

    def test_path_must_be_string(self):
        expected_message = 'Inappropriate argument type for path; str expected'

        bad_values = (123, [], (), 12.34)

        for value in bad_values:
            with self.assertRaises(TypeError) as m:
                ApiListingReference(**self.create_parameters(path=value))
            self.assertEqual(expected_message, m.exception.message)

    def test_missing_optional_parameters_are_not_in_dict_representation(self):
        for parameter in self.optional_parameters:
            params = self.create_parameters(without=parameter)

            ref_dict = ApiListingReference(**params).as_dict()

            self.assertNotIn(parameter, ref_dict)

    def create_default_parameters(self):
        return {
            'path': 'path',
            'description': 'description'
        }


class ResourceListingTest(unittest.TestCase, ParameterProviderMixin):
    optional_parameters = ('description', 'info')

    def test_description_is_optional(self):
        p = self.create_parameters(without='description')

        ResourceListing(**p)

    def test_info_is_optional(self):
        p = self.create_parameters(without='info')

        ResourceListing(**p)

    def test_missing_optional_parameters_are_not_in_dict_representation(self):
        for parameter in self.optional_parameters:
            params = self.create_parameters(without=parameter)

            ref_dict = ResourceListing(**params).as_dict()

            self.assertNotIn(parameter, ref_dict)

    def test_bad_apis_argument(self):
        exception_message = ('Inappropriate argument type for apis. '
                             'Iterable of ApiListingReference expected.')

        api_ref = ApiListingReference('path1', 'descr1')
        bad_api_ref = 123

        apis_parameters = (
            'bad api ref',
            bad_api_ref,
            [api_ref, 'bad api ref'],
            (bad_api_ref, api_ref),
        )

        for apis_parameter in apis_parameters:
            with self.assertRaises(TypeError) as m:
                p = self.create_parameters(apis=apis_parameter)
                ResourceListing(**p)
            self.assertEqual(exception_message, m.exception.message)

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
