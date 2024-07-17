import face_recognition
from attendance.models import Person
from django.core.files.base import ContentFile
import numpy as np

def generate_face_encodings():
    persons = Person.objects.all()
    for person in persons:
        image = face_recognition.load_image_file(person.image.path)
        encoding = face_recognition.face_encodings(image)[0]
        person.face_encoding = ContentFile(encoding.tobytes())
        person.save()
