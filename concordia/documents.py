from django.contrib.auth.models import User
from django_elasticsearch_dsl import DocType, Index, fields

from .models import Transcription

user = Index("users")
user.settings(number_of_shards=1, number_of_replicas=0)

transcription = Index("transcriptions")
transcription.settings(number_of_shards=1, number_of_replicas=0)


@user.doc_type
class UserDocument(DocType):
    class Meta:
        model = User

        fields = ["last_login", "date_joined", "username"]


@transcription.doc_type
class TranscriptionDocument(DocType):
    asset = fields.ObjectField(
        properties={
            "title": fields.TextField(),
            "slug": fields.TextField(),
            "transcription_status": fields.TextField(),
            "item": fields.ObjectField(
                properties={
                    "item_id": fields.TextField(),
                    "project": fields.ObjectField(
                        properties={
                            "slug": fields.TextField(),
                            "campaign": fields.ObjectField(
                                properties={"slug": fields.TextField()}
                            ),
                        }
                    ),
                }
            ),
        }
    )
    user = fields.ObjectField(properties={"username": fields.TextField()})
    reviewed_by = fields.ObjectField(properties={"username": fields.TextField()})
    supersedes = fields.ObjectField(properties={"id": fields.IntegerField()})

    class Meta:
        model = Transcription

        fields = [
            "id",
            "created_on",
            "updated_on",
            "text",
            "accepted",
            "rejected",
            "submitted",
        ]
