from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Pizza(models.Model):
    name = models.CharField(max_length=30)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        # topping_string=''
        # for topping in self.toppings.all():
        #     topping_string += topping.name
        #     topping_string += ', '
        # toppings_string = topping_string[:-2]
        # return '{} ({})'.format(
        #     self.name,
        #     toppings_string
        # )
        #
        # [topping for topping in self.toppings.all()]
        topping_string = ', '.join([topping.name for topping in self.toppings.all()])
        return '{}({})'.format(self.name, topping_string)

    class Meta:
        ordering = ('name',)
