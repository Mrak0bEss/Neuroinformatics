from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Создаём экземпляр приложения FastAPI
app = FastAPI(title="Beer Recommendation API", description="Рекомендуем сорта пива на основе ваших данных", version="1.0")

# Загружаем модель
model_path = "model.joblib"
model = joblib.load(model_path)

# Определите доступные категории (гендер и локация)
valid_genders = {"м": "Male", "ж": "Female"}
valid_locations = ["Москва", "Питер", "Казань", "Белгород"]

# Определяем Pydantic-модель для входных данных
class UserData(BaseModel):
    age: int
    gender: str
    location: str

@app.post("/recommend/", summary="Получить рекомендации", description="Отправьте данные пользователя, чтобы получить рекомендации по пиву.")
async def recommend_beers(user_data: UserData):
    # Проверка валидности входных данных
    if user_data.gender not in valid_genders:
        raise HTTPException(status_code=400, detail="Некорректный пол. Используйте 'м' или 'ж'.")

    if user_data.location not in valid_locations:
        raise HTTPException(status_code=400, detail=f"Некорректный город. Используйте один из {valid_locations}.")

    # Подготовка данных пользователя
    gender_encoded = valid_genders[user_data.gender]
    user_input = pd.DataFrame([
        {
            "age": user_data.age,
            "gender": gender_encoded,
            "location": user_data.location,
        }
    ])

    # Список признаков, использованных при обучении модели
    feature_names = ["age", "gender_Male", "gender_Female", "location_Москва", "location_Питер", "location_Казань", "location_Белгород"]

    # One-hot encoding
    user_input = pd.get_dummies(user_input, columns=["gender", "location"])
    user_input = user_input.reindex(columns=feature_names, fill_value=0)

    # Получение предсказаний
    try:
        predictions_proba = model.predict_proba(user_input)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка предсказания: {str(e)}")

    # Топ-5 сортов пива
    top_5_indices = predictions_proba.argsort()[-5:][::-1]
    top_5_beers = [int(idx) for idx in top_5_indices]

    # Формирование результата
    recommendations = [{"beer_id": beer_id, "beer_name": f"Пиво {beer_id}"} for beer_id in top_5_beers]

    return {"recommendations": recommendations}


@app.get("/", summary="Главная страница")
async def root():
    return {"message": "Добро пожаловать в Beer Recommendation API! Перейдите на /docs для взаимодействия с API."}
