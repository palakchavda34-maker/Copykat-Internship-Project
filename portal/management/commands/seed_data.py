from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import Student, Company, Internship, Application


class Command(BaseCommand):
    help = 'Seeds dummy data for Students, Companies, Internships, and Applications'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding database with dummy data...'))

        # 1. Create Superuser for Django Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@internship.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created Superuser: admin / admin123'))
        else:
            self.stdout.write('Superuser "admin" already exists.')

        # 2. Create Dummy Students
        students_data = [
            {'name': 'Rahul Sharma', 'email': 'rahul.sharma@example.com', 'college': 'IIT Bombay'},
            {'name': 'Priya Verma', 'email': 'priya.verma@example.com', 'college': 'NIT Trichy'},
            {'name': 'Amit Patel', 'email': 'amit.patel@example.com', 'college': 'BITS Pilani'},
            {'name': 'Sneha Gupta', 'email': 'sneha.gupta@example.com', 'college': 'DTU Delhi'},
        ]

        created_students = []
        for data in students_data:
            student, created = Student.objects.get_or_create(
                email=data['email'],
                defaults={'name': data['name'], 'college': data['college']}
            )
            if created:
                student.set_password('student123')
                student.save()
            created_students.append(student)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(created_students)} Students.'))

        # 3. Create Dummy Companies
        companies_data = [
            {'company_name': 'TechCorp Solutions', 'email': 'careers@techcorp.com', 'location': 'Bangalore', 'approved': True},
            {'company_name': 'CloudInnovate Inc', 'email': 'hr@cloudinnovate.io', 'location': 'Hyderabad', 'approved': True},
            {'company_name': 'DataForge Labs', 'email': 'contact@dataforge.com', 'location': 'Pune', 'approved': False},
            {'company_name': 'NextGen Systems', 'email': 'jobs@nextgen.com', 'location': 'Remote', 'approved': True},
        ]

        created_companies = []
        for data in companies_data:
            company, created = Company.objects.get_or_create(
                email=data['email'],
                defaults={
                    'company_name': data['company_name'],
                    'location': data['location'],
                    'approved': data['approved']
                }
            )
            if created:
                company.set_password('company123')
                company.save()
            created_companies.append(company)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(created_companies)} Companies.'))

        # 4. Create Dummy Internships
        internships_data = [
            {
                'company': created_companies[0],  # TechCorp
                'title': 'Django Backend Intern',
                'description': 'Develop scalable RESTful APIs using Django REST Framework and PostgreSQL.',
                'location': 'Bangalore (Hybrid)',
                'stipend': 25000.00
            },
            {
                'company': created_companies[0],  # TechCorp
                'title': 'Frontend React Intern',
                'description': 'Build responsive user interfaces using React.js and modern CSS tooling.',
                'location': 'Bangalore',
                'stipend': 20000.00
            },
            {
                'company': created_companies[1],  # CloudInnovate
                'title': 'DevOps & Cloud Intern',
                'description': 'Automate deployment pipelines using Docker, Kubernetes, and AWS.',
                'location': 'Hyderabad',
                'stipend': 30000.00
            },
            {
                'company': created_companies[3],  # NextGen Systems
                'title': 'Full Stack Developer Intern',
                'description': 'Work across Python, JavaScript, and database architecture in a fast-paced environment.',
                'location': 'Remote',
                'stipend': 22000.00
            },
        ]

        created_internships = []
        for data in internships_data:
            internship, created = Internship.objects.get_or_create(
                company=data['company'],
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'location': data['location'],
                    'stipend': data['stipend']
                }
            )
            created_internships.append(internship)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(created_internships)} Internships.'))

        # 5. Create Dummy Applications
        applications_data = [
            {'student': created_students[0], 'internship': created_internships[0], 'status': 'Pending'},
            {'student': created_students[1], 'internship': created_internships[0], 'status': 'Accepted'},
            {'student': created_students[2], 'internship': created_internships[2], 'status': 'Pending'},
            {'student': created_students[3], 'internship': created_internships[3], 'status': 'Rejected'},
        ]

        created_apps_count = 0
        for data in applications_data:
            app, created = Application.objects.get_or_create(
                student=data['student'],
                internship=data['internship'],
                defaults={'status': data['status']}
            )
            if created:
                created_apps_count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created_apps_count} Applications.'))

        self.stdout.write(self.style.SUCCESS('Successfully completed dummy data seeding!'))
