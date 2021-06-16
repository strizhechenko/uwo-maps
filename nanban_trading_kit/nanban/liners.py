from datetime import datetime

from colorama import Fore

from .prints import wrap, header


class Liner:
    def __init__(self, way, src, dst):
        self.src = src
        self.dst = dst
        self.way = way

    def where(self, date):
        i = (date.hour * 60 + date.minute) % 120
        return {
            0 <= i < self.way: f'{self.src} to {self.dst}',
            self.way <= i < 60: f'Staying in {self.dst}',
            60 <= i < 60 + self.way: f'{self.dst} to {self.src}'
        }.get(True, f'Staying in {self.src}')

    def __iter__(self):
        now = datetime.now()
        for i in range(3):
            yield now
            if now.minute + self.way < 60:
                yield now.replace(minute=self.way)
            now = now.replace(hour=(0 if now.hour == 23 else now.hour + 1), minute=0)


def _print(place, date):
    print(wrap(date.time().strftime("%H:%M"), Fore.LIGHTRED_EX), place)


def liners():
    for liner in Liner(35, 'London', 'Nagasaki'), Liner(25, 'London', 'Colony'):
        header(f"{liner.src} <-> {liner.dst}")
        now = datetime.now()
        _print(liner.where(now), now)
        for i in range(3):
            try:
                now = now.replace(minute=(now.minute + liner.way))
                _print(liner.where(now), now)
            except ValueError:
                pass
            now = now.replace(hour=(0 if now.hour == 23 else now.hour + 1) % 24, minute=0)
            _print(liner.where(now), now)
