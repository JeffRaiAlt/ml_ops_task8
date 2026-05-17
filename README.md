# ML DevOps Project

Мониторинг и наблюдаемость в продакшене

## Задание 1
Определить ключевые бизнес- и технические метрики для ML-системы

[Дерево метрик](doc/architecture/0001-metrics-recommendation.md)

## Задание 2

Настроить мониторинг с использованием Prometheus, Grafana

Все необходимые сервисы расположены в каталоге 
monitoring-lab
[Мониторинг](monitoring-lab)

Скриншоты работы в каталоге 
[Скриншоты](doc/screenshots/monitoring)
- имитируем обычные запросы
http://localhost:8000/predict

- имитируем запросы с задержками
http://localhost:8000/predict?slow=true

Для alert была использована метрика `request_latency_seconds`, собранная как Prometheus Histogram.
На ее основе считается p95 latency:
```promql
histogram_quantile(
  0.95,
  sum(rate(request_latency_seconds_bucket[5m])) by (le)
)
```
[Экспортированный дашборд](monitoring-lab/export-Main.yaml)

## Задание 3
Обнаружить деградацию модели и дрифт.

[Дрифт](src/data-drift.py)
[Отчет](doc/drift)

```text
                      batch  accuracy  precision    recall        f1   roc_auc
0          reference_normal  0.991228   1.000000  0.986111  0.993007  1.000000
1            current_normal  0.991228   0.986111  1.000000  0.993007  0.997052
2  current_with_drift_x1000  0.377193   0.000000  0.000000  0.000000  0.500000
```
Для демонстрации data drift и деградации модели был использован встроенный датасет `breast_cancer`.
На нормальных данных была обучена модель Logistic Regression.
Данные были разделены на train, reference batch и current batch.
Затем current batch был искусственно изменен:

```python
X_current_drift = X_current * 1000
```
После такого изменения evidently обнаруживает data drift между reference_data и current_data;
качество модели на current_with_drift_x1000 падает по метрикам Accuracy, 
Precision, Recall, F1-score и ROC-AUC.

## Задание 4
Обеспечить качество данных с Data Quality Ops

```text
План был такой
1. Поднимаем DQOps и PostgreSQL в Docker.
2. Создаем таблицу в PostgreSQL через DBeaver.
3. Подключаем PostgreSQL как Data Source в DQOps.
4. Импортируем таблицу в DQOps.
5. Включаем schema checks.
6. Запускаем checks первый раз — фиксируем baseline.
7. Меняем структуру таблицы в PostgreSQL.
8. Запускаем checks второй раз.
9. DQOps видит schema drift и создает incident.
10. Делаем необходимые скриншоты
```
Я начал делать задачу [Качество данных](dqops-lab)
Но возникла проблема [проблема](doc/dqops/dqops-error.png)
причем ключом [регистрация](doc/dqops/try-get-key.png) она не лечится.
В качестве воспроизводимой альтернативы можно использовать PostgreSQL вместе  
с чем нибудь типа Soda Core или Great Expectations для демонстрации schema drift,
но в задании речи об этом нет, да и времени изучать это не осталось. По хорошему 
в задании не должны участвовать инструменты под лицензиями, а если все таки
по учебному плану должны, то студенты должны быть обеспечены ключами, 
это стандартная практика. 