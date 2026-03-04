import uuid
from django.db import models
from common.models import BaseModel

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    name = models.CharField(max_length=255)
    company_data = models.JSONField()

    class CompanyStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.name

class CompanyUserMembership(BaseModel):
    
    class UserRole(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="memberships"
    )
    user_role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.MEMBER
    )

    class Meta:
        db_table = "company_membership"
        unique_together = ("company", "user")
        indexes = [models.Index(fields=["company", "user"])]