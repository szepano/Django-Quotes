# from django.db import models

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, StringField, ListField, ReferenceField, BooleanField, EmailField

# Create your models here.

class Tag(EmbeddedDocument):
    name = StringField(required=True)


class Author(Document):
    name = StringField(required=True)
    born = StringField()
    born_in = StringField()
    desc = StringField()

    meta = {'collection': 'author'
    }

    def __str__(self):
        return self.name

class Quote(Document):
    quote = StringField(required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author, required=True)

    meta = {'collection': 'quote'
    }