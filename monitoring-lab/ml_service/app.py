import random
import time

from fastapi import FastAPI, Response
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST


app = FastAPI()


REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    buckets=(0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.0, 5.0),
)


@app.get("/predict")
def predict(slow: bool = False):
    start_time = time.time()

    try:
        # Имитация работы ML-модели.
        # Обычный режим: быстрый ответ.
        # slow=true: искусственно ломаем SLO.
        if slow:
            time.sleep(2)
        else:
            time.sleep(random.uniform(0.05, 0.3))

        return {
            "recommendations": [
                "film_101",
                "film_204",
                "film_309",
            ]
        }

    finally:
        REQUEST_LATENCY.observe(time.time() - start_time)


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )