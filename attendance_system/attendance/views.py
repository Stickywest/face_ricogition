from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person, Attendance
import face_recognition
import cv2
import numpy as np
from django.utils import timezone

# Home page view
def home(request):
    return render(request, 'home.html')

# Face scanning view
def scan_face(request):
    if request.method == 'POST':
        image = request.FILES['image']
        image_array = np.frombuffer(image.read(), np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        face_encodings = face_recognition.face_encodings(image)
        if not face_encodings:
            return JsonResponse({'status': 'no_face_detected'})

        face_encoding = face_encodings[0]
        
        persons = Person.objects.all()
        known_encodings = [np.array(eval(person.encoding)) for person in persons if person.encoding]
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = None

        if True in matches:
            first_match_index = matches.index(True)
            person = persons[first_match_index]
            name = person.name

            # Record attendance
            current_time = timezone.now()
            last_attendance = Attendance.objects.filter(person=person).order_by('-timestamp').first()
            action = 'IN' if not last_attendance or last_attendance.action == 'OUT' else 'OUT'
            
            Attendance.objects.create(person=person, action=action, timestamp=current_time)

            return JsonResponse({'status': 'success', 'name': name, 'action': action})
        
        return JsonResponse({'status': 'unknown_face'})

    return JsonResponse({'status': 'failed'})

# Class-based views for person management
class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'

class PersonCreateView(CreateView):
    model = Person
    fields = ['name', 'phone_number', 'email', 'role', 'image']
    template_name = 'person_form.html'
    success_url = reverse_lazy('person-list')

class PersonUpdateView(UpdateView):
    model = Person
    fields = ['name', 'phone_number', 'email', 'role', 'image']
    template_name = 'person_form.html'
    success_url = reverse_lazy('person-list')

class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'person_confirm_delete.html'
    success_url = reverse_lazy('person-list')

class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_list.html'
