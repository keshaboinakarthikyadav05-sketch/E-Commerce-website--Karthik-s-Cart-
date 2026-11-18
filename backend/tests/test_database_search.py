import hashlib
import hmac
import os
import sys
import tempfile
import unittest

from sqlalchemy.engine import URL

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import initialize_database
from app.models import Category, Product, db
from app.services.razorpay_service import RazorpayService
from seed import sample_products


class DatabaseSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()

        class TestConfig:
            TESTING = True
            SECRET_KEY = 'test-secret'
            JWT_SECRET_KEY = 'test-jwt-secret'
            RAZORPAY_KEY_SECRET = 'test-payment-secret'
            IS_PRODUCTION = False
            AUTO_INITIALIZE_DATABASE = True
            SQLALCHEMY_DATABASE_URI = URL.create(
                'sqlite',
                database=os.path.join(cls.temp_dir.name, 'shopora-test.db'),
            ).render_as_string(hide_password=False)
            SQLALCHEMY_TRACK_MODIFICATIONS = False

        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            cls.initial_product_count = Product.query.count()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.engine.dispose()
        cls.temp_dir.cleanup()

    def test_startup_creates_sqlite_tables_and_sample_catalog(self):
        database_path = os.path.join(self.temp_dir.name, 'shopora-test.db')
        self.assertTrue(os.path.isfile(database_path))

        with self.app.app_context():
            self.assertEqual(self.initial_product_count, len(sample_products.PRODUCTS_DATA))
            self.assertGreaterEqual(Product.query.count(), self.initial_product_count)
            self.assertEqual(Category.query.count(), len(sample_products.CATEGORIES_DATA))

    def test_reinitialization_is_idempotent_and_preserves_existing_products(self):
        with self.app.app_context():
            initial_count = Product.query.count()
            category = Category.query.first()
            custom_product = Product(
                name='Customer Created Product',
                slug='customer-created-product',
                description='An existing product must not be deleted by startup.',
                category_id=category.id,
                brand='Local Brand',
                original_price=100,
                discounted_price=90,
                discount_percent=10,
                stock=5,
            )
            db.session.add(custom_product)
            db.session.commit()

        initialize_database(self.app)

        with self.app.app_context():
            self.assertEqual(Product.query.count(), initial_count + 1)
            self.assertIsNotNone(Product.query.filter_by(slug='customer-created-product').first())

    def test_search_covers_name_brand_category_and_description(self):
        searches = {
            'iPhone': 'Apple iPhone',
            'Samsung': 'Samsung',
            'smartphones': 'Samsung Galaxy',
            'advanced stretch': "Levi's 511",
            'Jeans': 'Jeans',
        }
        for query, expected_text in searches.items():
            with self.subTest(query=query):
                response = self.client.get('/api/products/search', query_string={'q': query})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.get_json()['success'])
                self.assertTrue(any(expected_text.lower() in product['name'].lower()
                                    for product in response.get_json()['products']))

    def test_suggestions_health_and_development_reset(self):
        suggestions = self.client.get(
            '/api/products/search/suggestions',
            query_string={'q': 'iphone'},
        )
        self.assertEqual(suggestions.status_code, 200)
        self.assertTrue(suggestions.get_json()['suggestions'])

        health = self.client.get('/api/health')
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json()['database'], 'connected')

        reset = self.app.test_cli_runner().invoke(args=['reset-db'])
        self.assertEqual(reset.exit_code, 0, reset.output)
        with self.app.app_context():
            self.assertEqual(Product.query.count(), len(sample_products.PRODUCTS_DATA))

    def test_simulated_payment_verification_checks_signature_and_is_dev_only(self):
        order_id = 'order_test_example'
        payment_id = 'pay_test_example'
        signature = hmac.new(
            b'test-payment-secret',
            f'{order_id}|{payment_id}'.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

        with self.app.app_context():
            self.assertTrue(RazorpayService.verify_payment_signature(
                order_id, payment_id, signature
            ))
            self.assertFalse(RazorpayService.verify_payment_signature(
                order_id, payment_id, 'invalid-signature'
            ))
            self.app.config['IS_PRODUCTION'] = True
            self.assertFalse(RazorpayService.verify_payment_signature(
                order_id, payment_id, signature
            ))
            self.app.config['IS_PRODUCTION'] = False

    def test_suggestions_empty_results_pagination_and_category_alias(self):
        empty_suggestions = self.client.get('/api/products/search/suggestions')
        self.assertEqual(empty_suggestions.status_code, 200)
        self.assertEqual(empty_suggestions.get_json()['suggestions'], [])

        no_results = self.client.get('/api/products', query_string={'q': 'not-a-real-product'})
        self.assertEqual(no_results.status_code, 200)
        self.assertEqual(no_results.get_json()['products'], [])

        invalid_page = self.client.get('/api/products', query_string={'page': '0'})
        self.assertEqual(invalid_page.status_code, 400)
        invalid_limit = self.client.get('/api/products', query_string={'limit': '101'})
        self.assertEqual(invalid_limit.status_code, 400)

        old_categories_route = self.client.get('/api/categories')
        product_categories_route = self.client.get('/api/products/categories')
        self.assertEqual(old_categories_route.status_code, 200)
        self.assertEqual(product_categories_route.status_code, 200)
        self.assertEqual(
            old_categories_route.get_json()['categories'],
            product_categories_route.get_json()['categories'],
        )


if __name__ == '__main__':
    unittest.main()
