import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


# Create your views here.
def index(request):
    err_msg = ""
    message = ""
    message_class = ""
    api_key = "09ebd22c28ba8c515344342f0e935b5d"

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"]
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={new_city}&appid={api_key}&units=metric"
                ).json()

                if r["cod"] == 200:
                    form.save()
                else:
                    err_msg = "City does not exist!"
            else:
                err_msg = "City already exists in the database!"

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "City added successfully!"
            message_class = "is-success"

    form = CityForm()
    cities = City.objects.all()
    cities_data = []

    for city in cities:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        ).json()

        weather_data = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }
        cities_data.append(weather_data)

    context = {
        "cities_data": cities_data,
        "form": form,
        "message": message,
        "message_class": message_class,
    }

    return render(request, "base/index.html", context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect("index")
