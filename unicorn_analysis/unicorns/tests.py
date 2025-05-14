from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from .models import UnicornCompany

class UnicornCompanyModelTest(TestCase):
    def setUp(self):
        UnicornCompany.objects.create(
            name="Test Unicorn",
            valuation=1000000000.00,
            industry="Tech",
            country="USA",
            founded_year=2015,
            description="A test unicorn company."
        )

    def test_unicorn_creation(self):
        unicorn = UnicornCompany.objects.get(name="Test Unicorn")
        self.assertEqual(unicorn.name, "Test Unicorn")
        self.assertEqual(unicorn.valuation, 1000000000.00)
        self.assertEqual(unicorn.industry, "Tech")
        self.assertEqual(unicorn.country, "USA")
        self.assertEqual(unicorn.founded_year, 2015)
        self.assertEqual(unicorn.description, "A test unicorn company.")

class HomeViewTest(TestCase):
    def setUp(self):
        UnicornCompany.objects.create(
            name="Test Unicorn 2",
            valuation=2000000000.00,
            industry="Finance",
            country="UK",
            founded_year=2018,
            description="Another test unicorn."
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_context(self):
        response = self.client.get(reverse('home'))
        self.assertIn('unicorns', response.context)
        self.assertEqual(len(response.context['unicorns']), 1)
        self.assertContains(response, "Test Unicorn 2")

class AdminAccessTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

    def test_admin_login(self):
        login = self.client.login(username='admin', password='adminpass')
        self.assertTrue(login)

    def test_admin_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/unicorns/unicorncompany/')
        self.assertEqual(response.status_code, 200)

class FrontendUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_homepage_loads(self):
        self.driver.get(self.live_server_url)
        self.assertIn("Unicorn Companies", self.driver.title)
        table = self.driver.find_element(By.TAG_NAME, 'table')
        self.assertIsNotNone(table)

    def test_table_contents(self):
        # Add a unicorn to the database
        UnicornCompany.objects.create(
            name="UI Test Unicorn",
            valuation=3000000000.00,
            industry="Healthcare",
            country="Canada",
            founded_year=2020,
            description="UI test unicorn company."
        )
        self.driver.get(self.live_server_url)
        body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("UI Test Unicorn", body_text)
