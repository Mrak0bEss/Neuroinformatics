from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import time

# URL вашего FastAPI сервиса
FASTAPI_URL = "http://app:8000"


def recommend_page(request):
    if request.method == "GET":
        return render(request, "recommend.html")
    elif request.method == "POST":
        try:
            user_data = json.loads(request.body.decode("utf-8"))
            response = requests.post(f"{FASTAPI_URL}/recommend/", json=user_data)
            response.raise_for_status()
            return JsonResponse(response.json(), safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)


# View для отображения списка доступного пива
def list_beers(request):
    try:
        response = requests.get(f"{FASTAPI_URL}/recommend/")
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import time

from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import time


@csrf_exempt
@never_cache
def recommend_beer(request):
    if request.method == "POST":
        try:
            # Получаем данные из POST-запроса
            user_data = json.loads(request.body.decode("utf-8"))

            # Обработка ручного ввода города
            if user_data.get("location") == "other" and "otherCity" in user_data:
                user_data["location"] = user_data["otherCity"]

            # Удаляем "otherCity" из данных
            user_data.pop("otherCity", None)

            # Отправляем данные в FastAPI
            response = requests.post(f"{FASTAPI_URL}/recommend/", json=user_data)
            response.raise_for_status()

            # Обработка успешного ответа
            recommendations = response.json().get("recommendations", [])

            # Извлекаем только данные из `availability`
            availability_list = [
                item for beer in recommendations for item in beer.get("availability", [])
            ]

            # Возвращаем данные
            return JsonResponse({"availability": availability_list}, safe=False, headers={"Cache-Control": "no-store"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

        except requests.exceptions.HTTPError as e:
            # Если FastAPI возвращает ошибку, передаем detail
            try:
                error_response = e.response.json()
                error_detail = error_response.get("detail", "An error occurred.")
            except (AttributeError, ValueError):
                error_detail = str(e)

            return JsonResponse({"error": error_detail}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Общая обработка ошибок сети
            return JsonResponse({"error": f"Request error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)


# View для добавления нового пива
def add_beer(request):
    if request.method == "POST":
        try:
            beer_data = {
                "name": request.POST.get("name"),
                "beer_type": request.POST.get("beer_type"),
                "model_id": int(request.POST.get("model_id", 0)),
                "stock": int(request.POST.get("stock", 0)),
            }
            response = requests.post(f"{FASTAPI_URL}/add_beer/", json=beer_data)
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def add_beer_page(request):
    return render(request, "add_beer.html")
