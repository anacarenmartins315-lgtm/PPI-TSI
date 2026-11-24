from base64 import b64encode
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import FundoImobiliario


class FundoImobiliarioAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('api:fundoimobiliario-list')
        self.user = get_user_model().objects.create_user(
            username='api-user',
            password='test-password',
        )
        FundoImobiliario.objects.create(
            codigo='HGLG11',
            setor='logistica',
            dividend_yield_medio_12m=Decimal('8.50'),
            vacancia_financeira=Decimal('1.20'),
            vacancia_fisica=Decimal('2.30'),
            quantidade_ativos=10,
            data_constituicao=date(2010, 3, 1),
        )
        FundoImobiliario.objects.create(
            codigo='HOSP11',
            setor='hospital',
            dividend_yield_medio_12m=Decimal('7.25'),
            vacancia_financeira=Decimal('0.00'),
            vacancia_fisica=Decimal('0.00'),
            quantidade_ativos=4,
            data_constituicao=date(2015, 6, 15),
        )
        FundoImobiliario.objects.create(
            codigo='XPTO11',
            setor='logistica',
            dividend_yield_medio_12m=Decimal('9.10'),
            vacancia_financeira=Decimal('2.00'),
            vacancia_fisica=Decimal('3.00'),
            quantidade_ativos=8,
            data_constituicao=date(2018, 8, 20),
        )
        FundoImobiliario.objects.create(
            codigo='MALL11',
            setor='hibrido',
            dividend_yield_medio_12m=Decimal('6.80'),
            vacancia_financeira=Decimal('4.00'),
            vacancia_fisica=Decimal('5.00'),
            quantidade_ativos=12,
            data_constituicao=date(2020, 1, 10),
        )

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_list_funds(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

    def test_basic_authentication_allows_access(self):
        credentials = b64encode(b'api-user:test-password').decode('ascii')

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION='Basic {}'.format(credentials),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_authentication_allows_access(self):
        self.assertTrue(self.client.login(
            username='api-user',
            password='test-password',
        ))

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filters_by_code_and_sector(self):
        self.authenticate()

        response = self.client.get(
            self.url,
            {'codigo': 'HGLG11', 'setor': 'logistica'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [item['codigo'] for item in response.data['results']],
            ['HGLG11'],
        )

    def test_search_filter_matches_code_and_sector(self):
        self.authenticate()

        code_response = self.client.get(self.url, {'search': 'hglg'})
        sector_response = self.client.get(self.url, {'search': 'hospital'})

        self.assertEqual(
            [item['codigo'] for item in code_response.data['results']],
            ['HGLG11'],
        )
        self.assertEqual(
            [item['codigo'] for item in sector_response.data['results']],
            ['HOSP11'],
        )

    def test_ordering_parameter_and_default_ordering(self):
        self.authenticate()

        default_response = self.client.get(self.url)
        ascending_response = self.client.get(
            self.url,
            {'ordering': 'dividend_yield_medio_12m'},
        )

        self.assertEqual(
            [item['codigo'] for item in default_response.data['results']],
            ['XPTO11', 'HGLG11'],
        )
        self.assertEqual(
            [item['codigo'] for item in ascending_response.data['results']],
            ['MALL11', 'HOSP11'],
        )

    def test_page_number_pagination_includes_navigation_metadata(self):
        self.authenticate()

        first_page = self.client.get(self.url)
        second_page = self.client.get(self.url, {'page': 2})

        self.assertEqual(first_page.data['count'], 4)
        self.assertIsNotNone(first_page.data['next'])
        self.assertIsNone(first_page.data['previous'])
        self.assertEqual(len(first_page.data['results']), 2)
        self.assertIsNotNone(second_page.data['previous'])
        self.assertEqual(len(second_page.data['results']), 2)

    def test_accepts_configured_date_input_formats(self):
        self.authenticate()

        response = self.client.post(
            self.url,
            {
                'codigo': 'DATE11',
                'setor': 'outros',
                'dividend_yield_medio_12m': '5.00',
                'vacancia_financeira': '1.00',
                'vacancia_fisica': '1.00',
                'quantidade_ativos': 1,
                'data_constituicao': '23/11/2020',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data_constituicao'], '2020-11-23')

    def test_rejects_unconfigured_date_input_format(self):
        self.authenticate()

        response = self.client.post(
            self.url,
            {
                'codigo': 'DATE11',
                'setor': 'outros',
                'dividend_yield_medio_12m': '5.00',
                'vacancia_financeira': '1.00',
                'vacancia_fisica': '1.00',
                'quantidade_ativos': 1,
                'data_constituicao': '2020.11.23',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_constituicao', response.data)
