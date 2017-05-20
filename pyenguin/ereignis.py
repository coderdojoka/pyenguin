import collections

__author__ = 'Mark Weinreuter'


class EreignisBearbeiter(object):
    def __init__(self):
        self.registrierte_bearbeiter = []
        self.hat_bearbeiter = False

    def registriere(self, bearbeiter):
        if not isinstance(bearbeiter, collections.Callable):
            raise AttributeError("Der Bearbeiter muss aufrufbar sein.")

        self.registrierte_bearbeiter.append(bearbeiter)
        self.hat_bearbeiter = True

    def entferne(self, bearbeiter):
        if bearbeiter in self.registrierte_bearbeiter:
            self.registrierte_bearbeiter.remove(bearbeiter)
        else:
            print("Bearbeiter war nicht registriert!")
            return

        self.hat_bearbeiter = len(self.registrierte_bearbeiter) > 0

    def __call__(self, *args, **kwargs):
        for bearbeiter in self.registrierte_bearbeiter:
            bearbeiter(*args, **kwargs)

    def entferne_alle(self):
        self.registrierte_bearbeiter.clear()
        self.hat_bearbeiter = False


class Ereignis(object):
    pass
