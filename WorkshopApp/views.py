from django.shortcuts import render, redirect, HttpResponse

from django.views import View

import datetime

from WorkshopApp import models

# Create your views here.


class CreateRoom(View):

    def get(self, request):
        return render(request, 'add_room.html')


    def post(self, request):

        name = request.POST.get('name', None)
        capacity = request.POST.get('capacity', None)
        available_projector = request.POST.get('projector', None)

        if not name or int(capacity) <= 0:
            return HttpResponse('Niepoprawne Dane!')

        room = models.Room(name=name, capacity=capacity,
                           available_projector=available_projector)
        room.save()
        return redirect('/show/rooms/')


class ShowRooms(View):

    def get(self, request):
        rooms = models.Room.objects.all()
        actual_date = datetime.date.today()
        str_date = f"{actual_date}"
        selected_date = request.GET.get('check_date', '')
        if selected_date:
            for room in rooms:
                if room.reservation_set.filter(date=selected_date):
                    room.reserved = True
                else:
                    room.reserved = False


        return render(request, 'show_rooms.html', {'rooms': rooms,
                                                   'actual_date': actual_date,
                                                   'selected_date': selected_date,
                                                   'str_date': str_date})


class RoomDetail(View):

    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        reservations = room.reservation_set.all().order_by('date')
        message = 'd'
        if not room.available_projector:
            message = 'n'
        return render(request, 'room.html', context={'room': room, 'reservations': reservations, 'projector': message})


class DeleteRoom(View):

    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        room.delete()
        return redirect('/show/rooms/')


class ModifyRoom(View):

    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        return render(request, 'modify_room.html', {'room': room})

    def post(self, request, room_id):
        name = request.POST.get('name', None)
        capacity = request.POST.get('capacity', None)
        available_projector = request.POST.get('projector', None)
        room = models.Room.objects.get(id=room_id)

        if not name or int(capacity) <= 0:
            return HttpResponse('Niepoprawne Dane!')

        room.name = name
        room.capacity = capacity
        room.available_projector = bool(available_projector)
        room.save()
        return redirect('/show/rooms/')


class ReserveRoom(View):

    def get(self, request, room_id):
        str_date = f"{datetime.date.today()}"
        return render(request, 'reserve_room.html', {'str_date': str_date})

    def post(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        comment = request.POST.get('comment', None)
        date = request.POST.get('date', None)
        actual_date = datetime.date.today()

        if date < str(actual_date):
            return HttpResponse('Nie mozesz zarezerwowac z data wsteczna.')

        reservation = models.Reservation(comment=comment, date=date, room=room)
        reservation.save()

        return redirect('/show/rooms/')
