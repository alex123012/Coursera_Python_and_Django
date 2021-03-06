from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Berserk(AbstractPositive):

    def get_positive_effects(self):
        return self.base.get_negative_effects() + ['Berserk']

    def get_stats(self):
        x = self.base.get_stats()
        x['Strength'] += 7
        x['Endurance'] += 7
        x['Agility'] += 7
        x['Luck'] += 7
        x['Perception'] -= 3
        x['Charisma'] -= 3
        x['Intelligence'] -= 3
        x['HP'] += 50
        return x


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        return self.base.get_negative_effects() + ['Blessing']

    def get_stats(self):
        x = self.base.get_stats()
        list_s = ['Strength', 'Perception', 'Endurance', 'Charisma',
                  'Intelligence', 'Agility', 'Luck']
        for i in list_s:
            x[i] += 2
        return x


class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Weakness(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Blessing']

    def get_stats(self):
        x = self.base.get_stats()
        for i in ['Strength', 'Endurance', 'Agility']:
            x[i] -= 4
        return x


class Curse(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']

    def get_stats(self):
        x = self.base.get_stats()
        list_s = ['Strength', 'Perception', 'Endurance',
                  'Charisma', 'Intelligence', 'Agility', 'Luck']
        for i in list_s:
            x[i] -= 2
        return x


class EvilEye(AbstractNegative):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']

    def get_stats(self):
        x = self.base.get_stats()
        x['Luck'] -= 10
        return x


if __name__ == "__main__":
    c = Hero()
    print(c.get_stats())
    c1 = Berserk(c)
    print(c1.get_stats())
    c2 = Berserk(c1)
    print(c2.get_stats())
    c2.base = c2.base.base
    print(c2.get_stats())
    c3 = Weakness(c2)
    print(c3.get_stats())
