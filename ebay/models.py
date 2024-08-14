from django.db import models
from member.models import Member


class EbayCategory(models.Model):
    category_id = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=255)
    category_tree_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name} (ID: {self.category_id})"


class EbayCategoryAspect(models.Model):
    category = models.ForeignKey(EbayCategory, on_delete=models.CASCADE, related_name='aspects')
    aspect_name = models.CharField(max_length=255)
    aspect_data_type = models.CharField(max_length=50, default='STRING')
    aspect_mode = models.CharField(max_length=50, default='REQUIRED')
    aspect_usage = models.CharField(max_length=50, default='RECOMMENDED')

    def __str__(self):
        return self.aspect_name


class ApiTest(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='api_tests')
    endpoint = models.CharField(max_length=255)  # New field for the API endpoint
    request_body = models.TextField()
    response_body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test by {self.member} at {self.created_at} to {self.endpoint}"


class EbayApiLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    request_headers = models.TextField()
    request_body = models.TextField(null=True, blank=True)
    response_status = models.IntegerField()
    response_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.timestamp} - {self.endpoint} - {self.request_method}'
