from django.shortcuts import  render, redirect, reverse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView , CreateView , UpdateView , DeleteView, DetailView)
from .models import Appoinment , Doctor , Patient
from .forms import DoctorForm , AppoinmentForm
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import datetime, timedelta



def signup (request):
    form = SignupForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        user = form.save()
        login(request , user)
        return redirect('Appoinment-create')
    
    return render(request , 'signup.html' , {'form':form})


class DoctorCreateView(UserPassesTestMixin, CreateView) :
    form_class = DoctorForm
    template_name = "Doctor_form.html"
    success_url = reverse_lazy('Doctor-create')
    def test_func(self):
        return self.request.user.is_staff


class Doctorslistview(ListView):
    model = Doctor
    template_name = "index.html" 
    login_url = reverse_lazy('login')
    

class AppointmentCreateView(CreateView):
    model = Appoinment
    form_class = AppoinmentForm
    template_name = "Appoinment_form.html"
    success_url = reverse_lazy("Appoinment-create")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # if form.fields.get('time') :
        #     reserved_times = Appoinment.objects.filter(booked=True).values_list('time', flat=True)
        #     choices = [(choice[0], choice[1]) for choice in form.fields['time'].choices if choice[0] not in reserved_times]
        #     form.fields['time'].choices = choices

            
        if form.fields.get('time') :
            current_time = datetime.now().strftime("%H:%M")
            choices = [(choice[0], choice[1]) for choice in form.fields['time'].choices if choice[0] >= current_time]
            form.fields['time'].choices = choices
        return form
    
     
       
            
            
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     if form.fields.get('time'):
    #         current_time = datetime.now().time()
    #         reserved_times = Appoinment.objects.filter(booked=True, time__gte=current_time).values_list('time', flat=True)
    #         choices = [(choice[0], choice[1]) for choice in form.fields['time'].choices if choice[0] not in reserved_times]
    #         form.fields['time'].choices = choices
    #     return form
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     if 'time' in form.fields and form.is_bound and form.is_valid() and 'duration' in form.fields:
    #         duration = int(form.cleaned_data['duration'])
    #         start_time = datetime.strptime(form.cleaned_data['time'], "%H:%M")
    #         end_time = (start_time + timedelta(minutes=duration)).strftime("%H:%M")
    #         reserved_times = Appoinment.objects.filter(booked=True, time__range=(start_time, end_time)).values_list('time', flat=True)
    #         choices = [(choice[0], choice[1]) for choice in form.fields['time'].choices if choice[0] not in reserved_times]
    #         form.fields['time'].choices = choices
    #     return form
    def form_valid(self, form):
        # Check if the appointment conflicts with existing appointments
        existing_appointments = Appoinment.objects.filter(
            doctor=form.cleaned_data['doctor'],
            date=form.cleaned_data['date'],
            time = form.cleaned_data['time'],
            booked=True
        )
        if existing_appointments.exists():
            # If an existing appointment exists on the same date, return an error message
            form.add_error(None, 'An appointment has already been booked for this date. Please choose another date.')
            return super().form_invalid(form)
        
        # Check if the appointment conflicts with existing appointments in terms of time and duration
        start_time = datetime.strptime(form.cleaned_data['time'], "%H:%M")
        end_time = (start_time + timedelta(minutes=form.cleaned_data['duration'])).strftime("%H:%M")
        overlapping_appointments = Appoinment.objects.filter(
            doctor=form.cleaned_data['doctor'],
            date=form.cleaned_data['date'],
            time__lt=end_time,
            end_time__gt=form.cleaned_data['time'],
            booked=True
        )
        if overlapping_appointments.exists():
            # If there are overlapping appointments, return an error message
            form.add_error(None, 'There is an overlap with existing appointments. Please choose another time slot or duration.')
            return super().form_invalid(form)
        
        # Check if the appointment time is in the future
        current_time = datetime.now().strftime("%H:%M")
        if form.cleaned_data['date'] == datetime.now().date() and form.cleaned_data['time'] < current_time:
            # If the appointment time is in the past, return an error message
            form.add_error(None, 'The appointment time cannot be in the past. Please choose another time.')
            return super().form_invalid(form)
        
        # If no conflicts and the appointment time is valid, create a new appointment
        form.instance.booked = True
        form.instance.end_time = end_time
        return super().form_valid(form)   

   
#     def form_valid(self, form):
#         # Check if the appointment conflicts with existing appointments
#         existing_appointments = Appoinment.objects.filter(
#             doctor=form.cleaned_data['doctor'],
#             date=form.cleaned_data['date'],
#             time=form.cleaned_data['time'],
#             booked=True
#         )
#         if existing_appointments.exists():
#             # If an existing appointment exists, return an error message
#             form.add_error(None, 'This appointment has already been booked. Please choose another time slot.')
#             return super().form_invalid(form)
        
#         # If no existing appointments, create a new appointment
#         form.instance.booked = True
#         return super().form_valid(form)

#     # def form_invalid(self, form):
#     #     form.add_error(None, "You can't book an appointment at this time.")
#     #     return super().form_invalid(form)
    

class Appoinmentlistview(UserPassesTestMixin, ListView):
    model = Appoinment
    template_name = "Appoinment_list.html" 
    def test_func(self):
        return self.request.user.is_staff  



class DoctorDetailView(UserPassesTestMixin, DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        appointments = Appoinment.objects.filter(doctor=doctor)
        context['appointments'] = appointments
        return context
    

#app = Flask(__name__)

# @app.route('/appoinment/doctor_time/<int:id>', methods=['GET'])

#def doctor_time(id):
    # doctor = Doctor.query.get_or_404(id)
    # appointments = doctor.appointments.all()
    
    # appointment_list = []
    # for appointment in appointments:
    #     appointment_data = {
    #         'doctor': appointment.doctor,
    #         'time': appointment.time
    #     }
    #     appointment_list.append(appointment_data)
    
        #return jsonify("text")
        # return render(id , 'Appoinment_form.html' , {'appointment_list':appointment_list})
    




