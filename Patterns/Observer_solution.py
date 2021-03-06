from abc import ABC, abstractmethod


class ObservableEngine:

    def __init__(self):
        self.subscribers = set()

    def subscribe(self, name):
        self.subscribers.add(name)

    def unsubscribe(self, name):
        if name in self.subscribers:
            self.subscribers.remove(name)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, achievement):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement['title'])


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = []

    def update(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)


if __name__ == '__main__':
    full = FullNotificationPrinter()
    short = ShortNotificationPrinter()
    eng = ObservableEngine()
    eng.subscribe(full)
    eng.subscribe(short)
    eng.notify({'f': 123})
    print(full.achievements, short.achievements)
