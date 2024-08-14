from django.contrib import admin
from .models import EbayCategory, EbayCategoryAspect, ApiTest, EbayApiLog

# Register your models here.
admin.site.register(EbayCategory)
admin.site.register(EbayCategoryAspect)
admin.site.register(ApiTest)
admin.site.register(EbayApiLog)
