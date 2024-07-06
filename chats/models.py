from uuid import UUID
from django.db import models
import uuid
from users.models import Profile


# Create your models here.
class DirectChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profiles = models.ManyToManyField(Profile)
