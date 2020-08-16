from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

line_of_cars = []

services = {
    'change_oil': {
        'description': 'Change oil',
        'duration': 2,
    },
    'inflate_tires': {
        'description': 'Inflate tires',
        'duration': 5,
    },
    'diagnostic': {
        'description': 'Get diagnostic',
        'duration': 30,
    },
}

cars_processed = []

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'services': services,
        }
        return render(request, 'tickets/menu.html', context)

class GetTicketView(View):
    def get(self, request, *args, **kwars):
        service_type = kwars['service_type']
        duration_service = services[service_type]["duration"]
        description = services[service_type]["description"]
        ticket = len(line_of_cars) + 1

        index = 0
        for i, car in enumerate(line_of_cars):
            index = i
            if duration_service >= services[car['service']]["duration"]:
                break
        else:
            index += 1

        line_of_cars.insert(index, {
            'ticket': ticket,
            'service': service_type,
            'duration': duration_service,
            'description': description,
        })

        duration_queue = 0
        for car in line_of_cars[index+1:]:
            duration_queue += car['duration']

        context = {
            'ticket': ticket,
            'time': duration_queue ,
        }
        return render(request, 'tickets/get_ticket.html', context)

class ProcessingView(View):
    def get(self, request, *args, **kwars):
        queue = {}
        for v in services.values():
            queue[v['description']] = 0

        for car in line_of_cars:
            queue[car['description']] = queue.get(car['description'],0) + 1
        
        context = {
            'queue': queue,
        }
        return render(request, 'tickets/processing.html', context)

    def post(self, *args, **kwars):
        global cars_processed
        car_processed = {}
        if len(line_of_cars) > 0:
            car_processed = line_of_cars.pop()
        
        cars_processed = [car_processed]
        return redirect('/next')

class NextView(View):
    def get(self, request, *args, **kwars):
        global cars_processed
        if len(cars_processed) > 0:
            next_car = cars_processed[-1]
        else:
            next_car = {}
        
        context = {
            # 'cars_processed': cars_processed,
            'next_car': next_car,
        }
        return render(request, 'tickets/next.html', context)