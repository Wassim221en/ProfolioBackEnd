from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date, datetime
import json
import tempfile
from PIL import Image
import io

from .models import Recommendation
from .services import RecommendationService
from .repositories import RecommendationRepository


class RecommendationModelTest(TestCase):
    """
    Test cases for Recommendation model.
    """

    def setUp(self):
        """Set up test data."""
        self.recommendation_data = {
            'recommender_name': 'Adel Abobacker',
            'recommender_title': 'Senior WordPress Developer',
            'recommender_company': 'Freelancer',
            'recommender_location': 'Syria',
            'recommendation_text': 'Wassim Alshami is an exceptional back-end developer with expertise in ASP.NET and problem-solving. He excels in performance optimization, scalable architecture, and high code quality. A great team player, he shares knowledge and tackles challenges efficiently. I highly recommend him!',
            'relationship': 'Colleague',
            'project_context': 'Web Development Projects',
            'linkedin_url': 'https://www.linkedin.com/in/adel-abobacker',
            'email': 'adel@example.com',
            'recommendation_date': date(2024, 7, 15),
            'rating': 5,
            'skills_mentioned': ['ASP.NET', 'Problem Solving', 'Performance Optimization', 'Scalable Architecture'],
            'is_featured': True,
            'is_public': True,
            'display_order': 1
        }

    def test_create_recommendation(self):
        """Test creating a recommendation."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)

        self.assertEqual(recommendation.recommender_name, 'Adel Abobacker')
        self.assertEqual(recommendation.rating, 5)
        self.assertTrue(recommendation.is_featured)
        self.assertTrue(recommendation.is_public)
        self.assertEqual(len(recommendation.skills_mentioned), 4)

    def test_recommendation_str_method(self):
        """Test string representation of recommendation."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        expected_str = "Recommendation from Adel Abobacker (Freelancer)"
        self.assertEqual(str(recommendation), expected_str)

    def test_short_recommendation_property(self):
        """Test short recommendation property."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        short_text = recommendation.short_recommendation

        if len(self.recommendation_data['recommendation_text']) > 150:
            self.assertTrue(short_text.endswith('...'))
            self.assertEqual(len(short_text), 153)  # 150 + '...'
        else:
            self.assertEqual(short_text, self.recommendation_data['recommendation_text'])

    def test_recommender_full_title_property(self):
        """Test recommender full title property."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        expected_title = "Senior WordPress Developer at Freelancer"
        self.assertEqual(recommendation.recommender_full_title, expected_title)

    def test_get_rating_display(self):
        """Test rating display method."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        rating_display = recommendation.get_rating_display()
        self.assertEqual(rating_display, "★★★★★")

    def test_get_skills_display(self):
        """Test skills display method."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        skills_display = recommendation.get_skills_display()
        expected_skills = "ASP.NET, Problem Solving, Performance Optimization, Scalable Architecture"
        self.assertEqual(skills_display, expected_skills)

    def test_soft_delete(self):
        """Test soft delete functionality."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        recommendation.soft_delete()

        self.assertTrue(recommendation.is_deleted)
        self.assertIsNotNone(recommendation.deleted_at)

    def test_restore(self):
        """Test restore functionality."""
        recommendation = Recommendation.objects.create(**self.recommendation_data)
        recommendation.soft_delete()
        recommendation.restore()

        self.assertFalse(recommendation.is_deleted)
        self.assertIsNone(recommendation.deleted_at)


class RecommendationRepositoryTest(TestCase):
    """
    Test cases for RecommendationRepository.
    """

    def setUp(self):
        """Set up test data."""
        self.repository = RecommendationRepository()
        self.recommendation_data = {
            'recommender_name': 'Adel Abobacker',
            'recommender_title': 'Senior WordPress Developer',
            'recommender_company': 'Freelancer',
            'recommender_location': 'Syria',
            'recommendation_text': 'Wassim Alshami is an exceptional back-end developer with expertise in ASP.NET and problem-solving.',
            'relationship': 'Colleague',
            'recommendation_date': date(2024, 7, 15),
            'rating': 5,
            'skills_mentioned': ['ASP.NET', 'Problem Solving'],
            'is_featured': True,
            'is_public': True,
            'display_order': 1
        }

    def test_create_recommendation(self):
        """Test creating recommendation through repository."""
        recommendation = self.repository.create(**self.recommendation_data)

        self.assertIsInstance(recommendation, Recommendation)
        self.assertEqual(recommendation.recommender_name, 'Adel Abobacker')

    def test_get_public_recommendations(self):
        """Test getting public recommendations."""
        # Create public recommendation
        self.repository.create(**self.recommendation_data)

        # Create private recommendation
        private_data = self.recommendation_data.copy()
        private_data['is_public'] = False
        private_data['recommender_name'] = 'Private Recommender'
        self.repository.create(**private_data)

        public_recommendations = self.repository.get_public_recommendations()
        self.assertEqual(public_recommendations.count(), 1)
        self.assertEqual(public_recommendations.first().recommender_name, 'Adel Abobacker')

    def test_get_featured_recommendations(self):
        """Test getting featured recommendations."""
        # Create featured recommendation
        self.repository.create(**self.recommendation_data)

        # Create non-featured recommendation
        non_featured_data = self.recommendation_data.copy()
        non_featured_data['is_featured'] = False
        non_featured_data['recommender_name'] = 'Non Featured'
        self.repository.create(**non_featured_data)

        featured_recommendations = self.repository.get_featured_recommendations()
        self.assertEqual(featured_recommendations.count(), 1)
        self.assertEqual(featured_recommendations.first().recommender_name, 'Adel Abobacker')

    def test_get_by_rating(self):
        """Test getting recommendations by rating."""
        # Create recommendations with different ratings
        for rating in [3, 4, 5]:
            data = self.recommendation_data.copy()
            data['rating'] = rating
            data['recommender_name'] = f'Recommender {rating}'
            self.repository.create(**data)

        high_rated = self.repository.get_by_rating(min_rating=4, max_rating=5)
        self.assertEqual(high_rated.count(), 2)

    def test_search_recommendations(self):
        """Test searching recommendations."""
        self.repository.create(**self.recommendation_data)

        # Search by recommender name
        results = self.repository.search_recommendations('Adel')
        self.assertEqual(results.count(), 1)

        # Search by company
        results = self.repository.search_recommendations('Freelancer')
        self.assertEqual(results.count(), 1)

        # Search by recommendation text
        results = self.repository.search_recommendations('ASP.NET')
        self.assertEqual(results.count(), 1)

    def test_get_by_company(self):
        """Test getting recommendations by company."""
        self.repository.create(**self.recommendation_data)

        results = self.repository.get_by_company('Freelancer')
        self.assertEqual(results.count(), 1)

    def test_get_by_skills(self):
        """Test getting recommendations by skills."""
        self.repository.create(**self.recommendation_data)

        results = self.repository.get_by_skills(['ASP.NET'])
        self.assertEqual(results.count(), 1)

        results = self.repository.get_by_skills(['Python'])
        self.assertEqual(results.count(), 0)

    def test_get_recommendations_stats(self):
        """Test getting recommendation statistics."""
        # Create multiple recommendations
        for i in range(3):
            data = self.recommendation_data.copy()
            data['recommender_name'] = f'Recommender {i}'
            data['rating'] = 4 + (i % 2)  # Ratings 4 and 5
            self.repository.create(**data)

        stats = self.repository.get_recommendations_stats()

        self.assertEqual(stats['total_recommendations'], 3)
        self.assertEqual(stats['featured_recommendations'], 3)
        self.assertGreater(stats['average_rating'], 4)


class RecommendationServiceTest(TestCase):
    """
    Test cases for RecommendationService.
    """

    def setUp(self):
        """Set up test data."""
        self.service = RecommendationService()
        self.recommendation_data = {
            'recommender_name': 'Adel Abobacker',
            'recommender_title': 'Senior WordPress Developer',
            'recommender_company': 'Freelancer',
            'recommender_location': 'Syria',
            'recommendation_text': 'Wassim Alshami is an exceptional back-end developer with expertise in ASP.NET and problem-solving.',
            'relationship': 'Colleague',
            'recommendation_date': date(2024, 7, 15),
            'rating': 5,
            'skills_mentioned': ['ASP.NET', 'Problem Solving'],
            'is_featured': True,
            'is_public': True
        }

    def test_create_recommendation(self):
        """Test creating recommendation through service."""
        recommendation = self.service.create_recommendation(self.recommendation_data)

        self.assertIsInstance(recommendation, Recommendation)
        self.assertEqual(recommendation.recommender_name, 'Adel Abobacker')

    def test_create_recommendation_with_skills_string(self):
        """Test creating recommendation with skills as string."""
        data = self.recommendation_data.copy()
        data['skills_mentioned'] = 'ASP.NET, Problem Solving, Django'

        recommendation = self.service.create_recommendation(data)

        self.assertEqual(len(recommendation.skills_mentioned), 3)
        self.assertIn('ASP.NET', recommendation.skills_mentioned)
        self.assertIn('Django', recommendation.skills_mentioned)

    def test_validation_errors(self):
        """Test validation errors in service."""
        # Test missing required fields
        invalid_data = {'recommender_name': 'Test'}

        with self.assertRaises(Exception):
            self.service.create_recommendation(invalid_data)

    def test_toggle_featured_status(self):
        """Test toggling featured status."""
        recommendation = self.service.create_recommendation(self.recommendation_data)
        original_status = recommendation.is_featured

        updated_recommendation = self.service.toggle_featured_status(str(recommendation.id))

        self.assertEqual(updated_recommendation.is_featured, not original_status)

    def test_get_public_recommendations(self):
        """Test getting public recommendations through service."""
        self.service.create_recommendation(self.recommendation_data)

        recommendations = self.service.get_public_recommendations()

        self.assertEqual(len(recommendations), 1)
        self.assertTrue(recommendations[0].is_public)


class RecommendationAPITest(APITestCase):
    """
    Test cases for Recommendation API endpoints.
    """

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.recommendation_data = {
            'recommender_name': 'Adel Abobacker',
            'recommender_title': 'Senior WordPress Developer',
            'recommender_company': 'Freelancer',
            'recommender_location': 'Syria',
            'recommendation_text': 'Wassim Alshami is an exceptional back-end developer with expertise in ASP.NET and problem-solving.',
            'relationship': 'Colleague',
            'recommendation_date': '2024-07-15',
            'rating': 5,
            'skills_mentioned': ['ASP.NET', 'Problem Solving'],
            'is_featured': True,
            'is_public': True
        }

    def test_list_recommendations(self):
        """Test listing recommendations."""
        # Create a recommendation
        Recommendation.objects.create(
            recommender_name='Test Recommender',
            recommender_title='Test Title',
            recommender_company='Test Company',
            recommendation_text='This is a test recommendation with more than fifty characters.',
            relationship='Colleague',
            recommendation_date=date.today(),
            rating=5,
            is_public=True
        )

        url = reverse('recommendations:recommendation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No pagination, so response.data is a list directly
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['recommender_name'], 'Test Recommender')

    def test_create_recommendation_authenticated(self):
        """Test creating recommendation when authenticated."""
        self.client.force_authenticate(user=self.user)

        url = reverse('recommendations:recommendation-list')
        response = self.client.post(url, self.recommendation_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_create_recommendation_unauthenticated(self):
        """Test creating recommendation when not authenticated."""
        url = reverse('recommendations:recommendation-list')
        response = self.client.post(url, self.recommendation_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_featured_recommendations(self):
        """Test getting featured recommendations."""
        # Create featured recommendation
        Recommendation.objects.create(
            recommender_name='Featured Recommender',
            recommender_title='Test Title',
            recommender_company='Test Company',
            recommendation_text='This is a featured recommendation with more than fifty characters.',
            relationship='Colleague',
            recommendation_date=date.today(),
            rating=5,
            is_featured=True,
            is_public=True
        )

        url = reverse('recommendations:recommendation-featured')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_get_stats(self):
        """Test getting recommendation statistics."""
        # Create some recommendations
        for i in range(3):
            Recommendation.objects.create(
                recommender_name=f'Recommender {i}',
                recommender_title='Test Title',
                recommender_company='Test Company',
                recommendation_text='This is a test recommendation with more than fifty characters.',
                relationship='Colleague',
                recommendation_date=date.today(),
                rating=5,
                is_public=True
            )

        url = reverse('recommendations:recommendation-stats')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['total_recommendations'], 3)

    def test_search_recommendations(self):
        """Test searching recommendations."""
        # Create a recommendation
        Recommendation.objects.create(
            recommender_name='Searchable Recommender',
            recommender_title='Test Title',
            recommender_company='Test Company',
            recommendation_text='This recommendation mentions Django and Python programming.',
            relationship='Colleague',
            recommendation_date=date.today(),
            rating=5,
            is_public=True
        )

        url = reverse('recommendations:recommendation-search')
        search_data = {'query': 'Django'}
        response = self.client.post(url, search_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def create_test_image(self):
        """Create a test image for upload tests."""
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )

    def test_upload_image_authenticated(self):
        """Test uploading recommender image when authenticated."""
        self.client.force_authenticate(user=self.user)

        # Create a recommendation first
        recommendation = Recommendation.objects.create(
            recommender_name='Test Recommender',
            recommender_title='Test Title',
            recommender_company='Test Company',
            recommendation_text='This is a test recommendation with more than fifty characters.',
            relationship='Colleague',
            recommendation_date=date.today(),
            rating=5,
            is_public=True
        )

        url = reverse('recommendations:recommendation-upload-image', kwargs={'pk': recommendation.id})
        image_file = self.create_test_image()

        response = self.client.post(url, {'image': image_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
