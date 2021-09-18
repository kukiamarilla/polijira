from django.db import models


class Horario(models.Model):
    """
    Horario Modela el horario de los miembros de un proyecto

    Args:
        models (Model): Hereda el modelo de Django
    Atributes:
        lunes (IntegerField): Horas trabajadas
        martes (IntegerField): Horas trabajadas
        miercoles (IntegerField): Horas trabajadas
        jueves (IntegerField): Horas trabajadas
        viernes (IntegerField): Horas trabajadas
        sabado (IntegerField): Horas trabajadas
        domingo (IntegerField): Horas trabajadas
    """
    lunes = models.IntegerField(default=0)
    martes = models.IntegerField(default=0)
    miercoles = models.IntegerField(default=0)
    jueves = models.IntegerField(default=0)
    viernes = models.IntegerField(default=0)
    sabado = models.IntegerField(default=0)
    domingo = models.IntegerField(default=0)

    def por_semana(self):
        """
        por_semana Calcula las horas trabajadas en una semana

        Returns:
            int: Horas trabajadas
        """
        sum = 0
        for semana in self.to_array():
            sum += semana
        return semana

    def to_array(self):
        """
        to_array Pone todos los atributos de la clase en una lista

        Returns:
            list: Lista de todos los atributos de horario
        """
        lista = []
        lista.append(self.lunes)
        lista.append(self.martes)
        lista.append(self.miercoles)
        lista.append(self.jueves)
        lista.append(self.viernes)
        lista.append(self.sabado)
        lista.append(self.domingo)
        return lista
