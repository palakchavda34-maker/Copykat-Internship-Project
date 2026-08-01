from rest_framework import serializers
from .models import Student, Company, Internship, Application


# ==========================================
# STUDENT SERIALIZERS
# ==========================================

class StudentSerializer(serializers.ModelSerializer):
    """Serialize student profile data.

    This serializer is used for public student responses and does not expose
    password fields.
    """

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'college')


class StudentRegisterSerializer(serializers.ModelSerializer):
    """Register a new student and hash the provided raw password."""
    password = serializers.CharField(write_only=True, min_length=6)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'college', 'password')

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(raw_password)
        student.save()
        return student


class StudentLoginSerializer(serializers.Serializer):
    """Authenticate a student by verifying email and password."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not student.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        attrs['student'] = student
        return attrs


# ==========================================
# COMPANY SERIALIZERS
# ==========================================

class CompanySerializer(serializers.ModelSerializer):
    """Serialize company profile data without exposing passwords."""

    class Meta:
        model = Company
        fields = ('id', 'company_name', 'email', 'location', 'approved')


class CompanyApprovalSerializer(serializers.ModelSerializer):
    """Permit updating only the company approval status."""

    class Meta:
        model = Company
        fields = ('id', 'approved')
        read_only_fields = ('id',)


class CompanyRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Company
        fields = ('id', 'company_name', 'email', 'location', 'password')

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        company = Company(**validated_data)
        company.set_password(raw_password)
        company.approved = False  # Default: requires admin approval
        company.save()
        return company


class CompanyLoginSerializer(serializers.Serializer):
    """Validate credentials for company login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            company = Company.objects.get(email=email)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not company.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        attrs['company'] = company
        return attrs


# ==========================================
# INTERNSHIP SERIALIZERS
# ==========================================

class InternshipSerializer(serializers.ModelSerializer):
    """Serialize internship data and include the posting company name."""
    company_name = serializers.ReadOnlyField(source='company.company_name')

    class Meta:
        model = Internship
        fields = ('id', 'company', 'company_name', 'title', 'description', 'location', 'stipend', 'created_at')

    def validate_company(self, value):
        if not value.approved:
            raise serializers.ValidationError(
                "Unapproved company cannot create or update internships."
            )
        return value


# ==========================================
# APPLICATION SERIALIZERS
# ==========================================

class ApplicationSerializer(serializers.ModelSerializer):
    """Serialize internship applications and expose student/internship details."""
    student_name = serializers.ReadOnlyField(source='student.name')
    student_email = serializers.ReadOnlyField(source='student.email')
    college = serializers.ReadOnlyField(source='student.college')
    internship_title = serializers.ReadOnlyField(source='internship.title')
    company_name = serializers.ReadOnlyField(source='internship.company.company_name')
    status = serializers.CharField(read_only=True)
    applied_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Application
        fields = (
            'id', 'student', 'student_name', 'student_email', 'college',
            'internship', 'internship_title', 'company_name',
            'status', 'applied_on'
        )

    def validate(self, attrs):
        student = attrs.get('student')
        internship = attrs.get('internship')
        if student and internship and Application.objects.filter(
            student=student,
            internship=internship
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this internship."
            )
        return attrs

    def create(self, validated_data):
        validated_data['status'] = 'Pending'
        return super().create(validated_data)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'status')

    def validate_status(self, value):
        allowed = ['Pending', 'Accepted', 'Rejected']
        if value not in allowed:
            raise serializers.ValidationError(
                "Status must be one of: Pending, Accepted, Rejected."
            )
        return value


class StudentDashboardSerializer(serializers.Serializer):
    """Serialize student dashboard overview counts."""
    total_internships_applied = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()


class CompanyDashboardSerializer(serializers.Serializer):
    """Serialize company dashboard overview counts."""
    total_internships_posted = serializers.IntegerField()
    total_applications_received = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()
