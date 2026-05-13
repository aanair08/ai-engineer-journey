def get_weather(city):
    weather_data = {
        "kerala": "Rainy, 28C",
        "bangalore": "Cloudy, 24C",
        "delhi": "Hot, 36C"
    }

    return weather_data.get(city.lower(), "Weather not found")


def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation"