from django.db import models


class Horario(models.Model):
    lunes = models.IntegerField(default=0)
    martes = models.IntegerField(default=0)
    miercoles = models.IntegerField(default=0)
    jueves = models.IntegerField(default=0)
    viernes = models.IntegerField(default=0)
    sabado = models.IntegerField(default=0)
    domingo = models.IntegerField(default=0)

    def por_semana(self):
        sum = 0
        for semana in self.to_array():
            sum += semana
        return semana

    def to_array(self):
        lista = []
        lista.append(self.lunes)
        lista.append(self.martes)
        lista.append(self.miercoles)
        lista.append(self.jueves)
        lista.append(self.viernes)
        lista.append(self.sabado)
        lista.append(self.domingo)
        return lista
