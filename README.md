# Firome

Утилита, позволяющая добавить к данным вело тренировки маршрут, 
выгруженный из стороннего источника, например, Strava Routes или Komoot.

Точки маршрута привязываются к тренировке по расстоянию от начала пути.

## Использование

```shell
cd firome/

python -m firome --route test/2024-05-21_1597851131.gpx --recording test/40B032FC.fit
```

[Пример результата](https://www.strava.com/activities/11471378450)

## Данные

### Из FIT файла выгружаются только записи физической активности: 

- Время _(обязательное значение)_
- Расстояние _(обязательное значение)_
- Скорость
- Мощность
- Пульс
- Каденс

Не выгружается заголовок (расчёт на загрузку в Strava, где все данные заголовка) всё равно расчитываются.

### Из GPX файла с маршрутом выгружаются:

- Позиция _(обязательное значение)_
- Расстояние _(обязательное значение)_
- Высота на уровнем моря _(обязательное значение)_

Обычно файлы маршрута содержат намного меньше точек, чем файлы с активностью, поэтому трек на прямых участках немного "рваный".

## Выходные значения

Поддерживаемые форматы результата:

- TCX