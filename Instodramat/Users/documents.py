from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Profile
from django.contrib.auth.models import User


@registry.register_document
class ProfileDocument(Document):
    # Add username to search
    user = fields.ObjectField(properties={
        'username': fields.TextField()
    })
    class Index:
        name = 'profile'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Profile
        fields = [
            'first_name',
            'last_name',
        ]
        related_models = [
            User
        ]
