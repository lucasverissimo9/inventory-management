from django.db import models
import uuid

class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    company_key = models.UUIDField(default=uuid.uuid4, null=False, editable=False, unique=True, db_index=True)
    company_data = models.JSONField(blank=False, null=False)

    class CompanyStatusChoices(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"

    status = models.CharField(
        max_length=20,
        choices=CompanyStatusChoices.choices,
        default=CompanyStatusChoices.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)


