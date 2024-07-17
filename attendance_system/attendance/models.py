from django.db import models
import face_recognition

class Person(models.Model):
    ROLE_CHOICES = [
        ('Attachee', 'Attachee'),
        ('Staff', 'Staff'),
        ('Casual Worker', 'Casual Worker'),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='images/')
    encoding = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate face encoding when saving the Person instance
        if self.image and not self.encoding:
            image = face_recognition.load_image_file(self.image)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.encoding = encodings[0].tolist()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    ACTION_CHOICES = [
        ('IN', 'Sign In'),
        ('OUT', 'Sign Out'),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    def __str__(self):
        return f"{self.person.name} - {self.timestamp} - {self.action}"
