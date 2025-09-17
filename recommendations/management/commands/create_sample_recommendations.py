from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from recommendations.models import Recommendation


class Command(BaseCommand):
    help = 'Create sample recommendations for testing and demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample recommendations to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        sample_recommendations = [
            {
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
                'skills_mentioned': ['ASP.NET', 'Problem Solving', 'Performance Optimization', 'Scalable Architecture', 'Team Collaboration'],
                'is_featured': True,
                'is_public': True,
                'display_order': 1
            },
            {
                'recommender_name': 'Sarah Johnson',
                'recommender_title': 'Senior Software Engineer',
                'recommender_company': 'TechCorp Solutions',
                'recommender_location': 'United States',
                'recommendation_text': 'I had the pleasure of working with Wassim on several complex backend projects. His expertise in Django and Python is outstanding. He consistently delivers clean, maintainable code and has a deep understanding of software architecture principles. Wassim is also excellent at mentoring junior developers.',
                'relationship': 'Team Lead',
                'project_context': 'E-commerce Platform Development',
                'linkedin_url': 'https://www.linkedin.com/in/sarah-johnson',
                'email': 'sarah.johnson@techcorp.com',
                'recommendation_date': date(2024, 6, 10),
                'rating': 5,
                'skills_mentioned': ['Django', 'Python', 'Software Architecture', 'Code Quality', 'Mentoring'],
                'is_featured': True,
                'is_public': True,
                'display_order': 2
            },
            {
                'recommender_name': 'Ahmed Hassan',
                'recommender_title': 'DevOps Engineer',
                'recommender_company': 'CloudTech Inc',
                'recommender_location': 'Egypt',
                'recommendation_text': 'Wassim demonstrated exceptional skills in backend development and system design during our collaboration. His ability to optimize database queries and implement efficient caching strategies significantly improved our application performance. He is also very knowledgeable about cloud technologies and containerization.',
                'relationship': 'Project Collaborator',
                'project_context': 'Microservices Migration',
                'linkedin_url': 'https://www.linkedin.com/in/ahmed-hassan',
                'email': 'ahmed.hassan@cloudtech.com',
                'recommendation_date': date(2024, 5, 20),
                'rating': 5,
                'skills_mentioned': ['Database Optimization', 'Caching', 'Cloud Technologies', 'Docker', 'Microservices'],
                'is_featured': False,
                'is_public': True,
                'display_order': 3
            },
            {
                'recommender_name': 'Maria Rodriguez',
                'recommender_title': 'Product Manager',
                'recommender_company': 'InnovateLab',
                'recommender_location': 'Spain',
                'recommendation_text': 'Working with Wassim was a fantastic experience. He has a unique ability to understand business requirements and translate them into technical solutions. His communication skills are excellent, and he always keeps stakeholders informed about project progress. The APIs he developed were robust and well-documented.',
                'relationship': 'Product Manager',
                'project_context': 'API Development for Mobile App',
                'linkedin_url': 'https://www.linkedin.com/in/maria-rodriguez',
                'email': 'maria.rodriguez@innovatelab.com',
                'recommendation_date': date(2024, 4, 15),
                'rating': 4,
                'skills_mentioned': ['API Development', 'Business Analysis', 'Communication', 'Documentation', 'Mobile Backend'],
                'is_featured': False,
                'is_public': True,
                'display_order': 4
            },
            {
                'recommender_name': 'David Chen',
                'recommender_title': 'CTO',
                'recommender_company': 'StartupXYZ',
                'recommender_location': 'Canada',
                'recommendation_text': 'Wassim joined our startup as a senior backend developer and quickly became an invaluable team member. His expertise in building scalable systems helped us handle rapid user growth. He introduced best practices for testing and deployment that significantly improved our development workflow. Highly recommended for any backend role.',
                'relationship': 'Direct Manager',
                'project_context': 'Startup Backend Infrastructure',
                'linkedin_url': 'https://www.linkedin.com/in/david-chen',
                'email': 'david.chen@startupxyz.com',
                'recommendation_date': date(2024, 3, 8),
                'rating': 5,
                'skills_mentioned': ['Scalable Systems', 'Testing', 'CI/CD', 'Best Practices', 'Startup Environment'],
                'is_featured': True,
                'is_public': True,
                'display_order': 5
            }
        ]

        created_count = 0
        for i in range(min(count, len(sample_recommendations))):
            recommendation_data = sample_recommendations[i]
            
            # Check if recommendation already exists
            if not Recommendation.objects.filter(
                recommender_name=recommendation_data['recommender_name'],
                recommender_company=recommendation_data['recommender_company']
            ).exists():
                
                recommendation = Recommendation.objects.create(**recommendation_data)
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created recommendation from {recommendation.recommender_name} '
                        f'at {recommendation.recommender_company}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Recommendation from {recommendation_data["recommender_name"]} '
                        f'at {recommendation_data["recommender_company"]} already exists'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} sample recommendations!'
            )
        )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    'You can now view the recommendations in the admin panel or through the API.'
                )
            )
