from django.core.management.base import BaseCommand
from decimal import Decimal

from portal.models import Student, Company, Internship, Application


class Command(BaseCommand):
    help = "Creates realistic dummy data for the internship portal"

    def handle(self, *args, **kwargs):

        # -------------------------
        # STUDENTS
        # -------------------------
        students_data = [
            ("Aarav Sharma", "aarav.sharma@gmail.com", "GTU"),
            ("Priya Patel", "priya.patel@gmail.com", "Nirma University"),
            ("Rohan Mehta", "rohan.mehta@gmail.com", "Ahmedabad University"),
            ("Ananya Shah", "ananya.shah@gmail.com", "DAIICT"),
            ("Karan Desai", "karan.desai@gmail.com", "LJ University"),
            ("Ishita Joshi", "ishita.joshi@gmail.com", "PDEU"),
            ("Dev Patel", "dev.patel@gmail.com", "CHARUSAT"),
            ("Manya Trivedi", "manya.trivedi@gmail.com", "Silver Oak University"),
            ("Yash Thakkar", "yash.thakkar@gmail.com", "GTU"),
            ("Neha Shah", "neha.shah@gmail.com", "Nirma University"),
        ]

        students = []

        for name, email, college in students_data:
            student, created = Student.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "college": college,
                },
            )

            if created:
                student.set_password("Student@123")
                student.save()

            students.append(student)

        self.stdout.write(
            self.style.SUCCESS(
                f"Students ready: {len(students)}"
            )
        )

        # -------------------------
        # COMPANIES
        # -------------------------
        companies_data = [
            ("TechNova Solutions", "hr@technova.com", "Ahmedabad"),
            ("InnovateX Technologies", "hr@innovatex.com", "Gandhinagar"),
            ("CodeCraft Labs", "hr@codecraft.com", "Ahmedabad"),
            ("PixelSoft Technologies", "hr@pixelsoft.com", "Surat"),
            ("NextGen Systems", "hr@nextgen.com", "Vadodara"),
        ]

        companies = []

        for company_name, email, location in companies_data:
            company, created = Company.objects.get_or_create(
                email=email,
                defaults={
                    "company_name": company_name,
                    "location": location,
                    "approved": True,
                },
            )

            if created:
                company.set_password("Company@123")
                company.save()

            companies.append(company)

        self.stdout.write(
            self.style.SUCCESS(
                f"Companies ready: {len(companies)}"
            )
        )

        # -------------------------
        # INTERNSHIPS
        # -------------------------
        internships_data = [
            (
                companies[0],
                "Python Developer Intern",
                "Work on Python and Django backend development, REST APIs and database integration.",
                "Ahmedabad",
                Decimal("15000.00"),
            ),
            (
                companies[0],
                "Full Stack Developer Intern",
                "Build web applications using modern frontend and backend technologies.",
                "Ahmedabad",
                Decimal("18000.00"),
            ),
            (
                companies[1],
                "Machine Learning Intern",
                "Assist in developing machine learning models and data processing pipelines.",
                "Gandhinagar",
                Decimal("20000.00"),
            ),
            (
                companies[1],
                "Data Analyst Intern",
                "Analyze datasets and prepare reports and dashboards for business teams.",
                "Gandhinagar",
                Decimal("14000.00"),
            ),
            (
                companies[2],
                "Backend Developer Intern",
                "Develop REST APIs and backend services using Python and Django.",
                "Ahmedabad",
                Decimal("16000.00"),
            ),
            (
                companies[2],
                "Software Testing Intern",
                "Perform manual and automated testing of web applications.",
                "Ahmedabad",
                Decimal("12000.00"),
            ),
            (
                companies[3],
                "Frontend Developer Intern",
                "Create responsive user interfaces using HTML, CSS and JavaScript.",
                "Surat",
                Decimal("15000.00"),
            ),
            (
                companies[3],
                "UI/UX Design Intern",
                "Design user-friendly interfaces and create prototypes for web applications.",
                "Surat",
                Decimal("10000.00"),
            ),
            (
                companies[4],
                "Java Developer Intern",
                "Work on Java-based applications and enterprise software development.",
                "Vadodara",
                Decimal("17000.00"),
            ),
            (
                companies[4],
                "Cloud Computing Intern",
                "Learn and work with cloud infrastructure, deployment and monitoring.",
                "Vadodara",
                Decimal("18000.00"),
            ),
        ]

        internships = []

        for company, title, description, location, stipend in internships_data:
            internship, created = Internship.objects.get_or_create(
                company=company,
                title=title,
                defaults={
                    "description": description,
                    "location": location,
                    "stipend": stipend,
                },
            )

            internships.append(internship)

        self.stdout.write(
            self.style.SUCCESS(
                f"Internships ready: {len(internships)}"
            )
        )

        # -------------------------
        # APPLICATIONS
        # -------------------------
        applications_data = [
            (students[0], internships[0], "Accepted"),
            (students[1], internships[0], "Pending"),
            (students[2], internships[1], "Accepted"),
            (students[3], internships[2], "Pending"),
            (students[4], internships[2], "Rejected"),
            (students[5], internships[3], "Accepted"),
            (students[6], internships[4], "Pending"),
            (students[7], internships[4], "Accepted"),
            (students[8], internships[5], "Rejected"),
            (students[9], internships[6], "Pending"),
            (students[0], internships[7], "Pending"),
            (students[2], internships[8], "Accepted"),
            (students[4], internships[9], "Pending"),
            (students[6], internships[1], "Rejected"),
            (students[8], internships[3], "Accepted"),
        ]

        applications = []

        for student, internship, status in applications_data:
            application, created = Application.objects.get_or_create(
                student=student,
                internship=internship,
                defaults={
                    "status": status,
                },
            )

            applications.append(application)

        self.stdout.write(
            self.style.SUCCESS(
                f"Applications ready: {len(applications)}"
            )
        )

        # -------------------------
        # FINAL SUMMARY
        # -------------------------
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("Dummy data setup completed successfully!")
        )
        self.stdout.write(f"Students: {Student.objects.count()}")
        self.stdout.write(f"Companies: {Company.objects.count()}")
        self.stdout.write(f"Internships: {Internship.objects.count()}")
        self.stdout.write(f"Applications: {Application.objects.count()}")