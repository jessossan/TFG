from django import forms
from datetime import datetime, date


# CRIADOR
class CreateBreederEventForm(forms.Form):
    """Formulario registro de un evento del criador"""

    # Campos requeridos por el Evento

    title = forms.CharField(max_length=25, label='Título')
    description = forms.CharField(max_length=200, label='Descripción')
    place = forms.CharField(max_length=50, label='Lugar')

    startDate = forms.DateField(label='Fecha de inicio')
    startTime = forms.TimeField(label='Hora de inicio')

    finishDate = forms.DateField(label='Fecha de fin')
    finishTime = forms.TimeField(label='Hora de fin')

    length = forms.TimeField(required=False, label='Duración')
    photo = forms.ImageField(required=False, label='Foto del evento')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            startDate = self.cleaned_data["startDate"]
            finishDate = self.cleaned_data["finishDate"]

            # Comprobamos que la fecha de comienzo no sea no sea una fecha pasada
            if (startDate < date.today()):
                raise forms.ValidationError(
                    "No se puede crear un evento con una fecha pasada")

            try:
                # Intenta sumar un dia
                tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

            except Exception as e:
                # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
                error = e.args[0]
                dayOutOfRange = ''.join(['day is out of range for month', ])
                monthOutOfRange = ''.join(['month must be in 1..12', ])

                if error == dayOutOfRange:
                    tomorrow = date(date.today().year, date.today().month + 1, 1)

                # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
                elif error == monthOutOfRange:
                    tomorrow = date(date.today().year + 1, 1, 1)

            # Comprobamos que la fecha de comienzo no sea menos de un día de antelación
            if (tomorrow == startDate) or startDate == date.today():
                raise forms.ValidationError(
                    "No se puede registrar una fecha con menos de un día de antelación")

            # Comprobamos que la fecha de fin sea posterior a la de comienzo
            if (finishDate < startDate):
                raise forms.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de comienzo")


class EditEventForm(forms.Form):
    """Formulario de edición de un evento del criador o de la asociacion"""

    # Campos requeridos por el Evento

    title = forms.CharField(max_length=25, label='Título')
    description = forms.CharField(max_length=200, label='Descripción')
    place = forms.CharField(max_length=50, label='Lugar')

    startDate = forms.DateField(label='Fecha de inicio')
    startTime = forms.TimeField(label='Hora de inicio')

    finishDate = forms.DateField(label='Fecha de fin')
    finishTime = forms.TimeField(label='Hora de fin')

    length = forms.TimeField(required=False, label='Duración')
    photo = forms.ImageField(required=False, label='Foto del evento')
    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            startDate = self.cleaned_data["startDate"]
            finishDate = self.cleaned_data["finishDate"]

            # Comprobamos que la fecha de comienzo del evento no sea no sea una fecha pasada
            if (startDate < date.today()):
                raise forms.ValidationError(
                    "No se puede editar un evento pasado")

            try:
                # Intenta sumar un dia
                tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

            except Exception as e:
                # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
                error = e.args[0]
                dayOutOfRange = ''.join(['day is out of range for month', ])
                monthOutOfRange = ''.join(['month must be in 1..12', ])

                if error == dayOutOfRange:
                    tomorrow = date(date.today().year, date.today().month + 1, 1)

                # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
                elif error == monthOutOfRange:
                    tomorrow = date(date.today().year + 1, 1, 1)

            # Comprobamos que la fecha de comienzo no sea menos de un día de antelación
            if tomorrow == startDate or startDate == date.today():
                raise forms.ValidationError(
                    "No se puede registrar una fecha con menos de un día de antelación")

            # Comprobamos que la fecha de fin sea posterior a la de comienzo
            if (finishDate < startDate):
                raise forms.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de comienzo")


# ASOCIACION

class CreateAssociationEventForm(forms.Form):
    """Formulario registro de un evento de la asociacion"""

    # Campos requeridos por el Evento

    title = forms.CharField(max_length=25, label='Título')
    description = forms.CharField(max_length=200, label='Descripción')
    place = forms.CharField(max_length=50, label='Lugar')

    startDate = forms.DateField(label='Fecha de inicio')
    startTime = forms.TimeField(label='Hora de inicio')

    finishDate = forms.DateField(label='Fecha de fin')
    finishTime = forms.TimeField(label='Hora de fin')

    length = forms.TimeField(required=False, label='Duración')
    photo = forms.ImageField(required=False, label='Foto del evento')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            startDate = self.cleaned_data["startDate"]
            finishDate = self.cleaned_data["finishDate"]

            # Comprobamos que la fecha de comienzo no sea no sea una fecha pasada
            if (startDate < date.today()):
                raise forms.ValidationError(
                    "No se puede crear un evento con una fecha pasada")

            try:
                # Intenta sumar un dia
                tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

            except Exception as e:
                # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
                error = e.args[0]
                dayOutOfRange = ''.join(['day is out of range for month', ])
                monthOutOfRange = ''.join(['month must be in 1..12', ])

                if error == dayOutOfRange:
                    tomorrow = date(date.today().year, date.today().month + 1, 1)

                # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
                elif error == monthOutOfRange:
                    tomorrow = date(date.today().year + 1, 1, 1)

            # Comprobamos que la fecha de comienzo no sea menos de un día de antelación
            if (tomorrow == startDate) or startDate == date.today():
                raise forms.ValidationError(
                    "No se puede registrar una fecha con menos de un día de antelación")

            # Comprobamos que la fecha de fin sea posterior a la de comienzo
            if (finishDate < startDate):
                raise forms.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de comienzo")
