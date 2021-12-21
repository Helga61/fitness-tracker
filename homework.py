from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: Any = ('Тип тренировки: {}; Длительность: {:.3f} ч.; '
                    + 'Дистанция: {:.3f} км; Ср. скорость: {:.3f} км/ч; '
                    + 'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(self.training_type, self.duration,
                                   self.distance, self.speed, self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories'
                                  + 'для каждого типа тренировок')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = type(self).__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        result = InfoMessage(training_type, duration,
                             distance, speed, calories)
        return result


class Running(Training):
    """Тренировка: бег."""

    COEFF_CAL_1: int = 18
    COEFF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        cal_kg = (self.COEFF_CAL_1 * self.get_mean_speed() - self.COEFF_CAL_2)
        cal_weight = cal_kg * self.weight
        spent_calories = (cal_weight / self.M_IN_KM
                          * (self.duration * self.MINUTES_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        cal_weight_1 = self.COEFF_CAL_1 * self.weight
        cal_weight_2 = self.COEFF_CAL_2 * self.weight
        calc_1 = (self.get_mean_speed() ** 2 // self.height) * cal_weight_2
        spent_calories = ((cal_weight_1 + calc_1)
                          * (self.duration * self.MINUTES_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.COEFF_1)
                          * self.COEFF_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_codes: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        name_class = training_codes[workout_type]
        return name_class(*data)
    except KeyError:
        print('Уточните тип тренировки!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
