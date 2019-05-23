from django.test import TestCase


class RadiusTest(TestCase):
    """Unit tests for store radius functionality."""

    def test_store_postcode_returns_response(self):
        """Test that known store postcode returns 200 response."""
        postcode = 'CT1 3TQ'
        response = self.client.get('/radius/{}/1'.format(postcode))
        self.assertEqual(response.status_code, 200)

    def test_non_store_postcode_returns_response(self):
        """Test that known non-store postcode returns 200 response."""
        postcode = 'NP7 5YA'
        response = self.client.get('/radius/{}/1'.format(postcode))
        self.assertEqual(response.status_code, 200)

    def test_invalid_store_postcode_returns_404(self):
        """Test that unknown postcode returns 404."""
        postcode = 'GU19 5DG'
        response = self.client.get('/radius/{}/1'.format(postcode))
        self.assertEqual(response.status_code, 404)

    def test_invalid_non_store_postcode_returns_404(self):
        """Test that non-compliant postcode format returns 404."""
        postcode = 'totally not a postcode'
        response = self.client.get('/radius/{}/1'.format(postcode))
        self.assertEqual(response.status_code, 404)

    def test_valid_radius_query_contains_itself(self):
        """Test that radius query for a store returns itself."""
        postcode = 'CT1 3TQ'
        response = self.client.get('/radius/{}/1'.format(postcode))
        response_postcodes = [x.postcode for x in response.context.get('locations')]
        self.assertIn(postcode, response_postcodes)

    def test_known_postcode_against_near_store(self):
        """Test a known postcode within given radius of store returns store."""
        postcode = 'CT1 3UP'
        store_postcode = 'CT1 3TQ'
        response = self.client.get('/radius/{}/1'.format(postcode))
        response_postcodes = [x.postcode for x in response.context.get('locations')]
        self.assertIn(store_postcode, response_postcodes)

    def test_store_postcode_orders_results_north_to_south(self):
        """Test the store response returns longitude in descending order."""
        postcode = 'NW1 9EX'
        expected_response = [-0.018139, -0.068434, -0.13693]
        response = self.client.get('/radius/{}/25000'.format(postcode))
        locations = [x.longitude for x in response.context.get('locations')]
        self.assertEqual(locations, expected_response)
