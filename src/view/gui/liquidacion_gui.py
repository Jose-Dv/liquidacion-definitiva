from datetime import datetime
from math import isfinite

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from model.logica_liquidacion import (
    DatosLiquidacion,
    calcular_detalle_liquidacion,
    sumar_conceptos_liquidacion,
)

from model.excepciones import (
    SalarioInvalidoError,
    FechaInvalidaError,
    TipoRetiroInvalidoError,
    VacacionesInvalidasError,
)


class LiquidacionApp(App):

    def build(self):
        self.title = "Liquidación definitiva"

        # Contenedor principal de la interfaz.
        contenedor = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        titulo = Label(
            text="Calculadora de liquidación definitiva",
            font_size=24,
            size_hint_y=None,
            height=60
        )
        contenedor.add_widget(titulo)

        # Formulario con dos columnas: etiqueta y campo.
        formulario = GridLayout(
            cols=2,
            spacing=10
        )

        # Tipo de retiro.
        formulario.add_widget(
            Label(text="Tipo de retiro:")
        )

        self.tipo_retiro = Spinner(
            text="Renuncia",
            values=(
                "Renuncia",
                "Despido con justa causa",
                "Despido sin justa causa"
            )
        )
        formulario.add_widget(self.tipo_retiro)

        # Salario mensual.
        formulario.add_widget(
            Label(text="Salario mensual:")
        )

        self.salario = TextInput(
            hint_text="Ejemplo: 3000000",
            multiline=False
        )
        formulario.add_widget(self.salario)

        # Fecha de ingreso.
        formulario.add_widget(
            Label(text="Fecha de ingreso:\nAAAA-MM-DD")
        )

        self.fecha_ingreso = TextInput(
            hint_text="Ejemplo: 2025-01-01",
            multiline=False
        )
        formulario.add_widget(self.fecha_ingreso)

        # Fecha de retiro.
        formulario.add_widget(
            Label(text="Fecha de retiro:\nAAAA-MM-DD")
        )

        self.fecha_retiro = TextInput(
            hint_text="Ejemplo: 2025-06-30",
            multiline=False
        )
        formulario.add_widget(self.fecha_retiro)

        # Vacaciones disfrutadas.
        formulario.add_widget(
            Label(text="Días de vacaciones disfrutados:")
        )

        self.vacaciones = TextInput(
            text="0",
            multiline=False
        )
        formulario.add_widget(self.vacaciones)

        contenedor.add_widget(formulario)

        # Botón conectado con el método calcular.
        # Fila de botones.
        botones = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=50,
        )

        boton_calcular = Button(text="Calcular liquidación")
        boton_calcular.bind(on_release=self.calcular)
        botones.add_widget(boton_calcular)

        boton_limpiar = Button(text="Limpiar")
        boton_limpiar.bind(on_release=self.limpiar)
        botones.add_widget(boton_limpiar)

        contenedor.add_widget(botones)

        # Espacio para presentar el resultado.
        self.resultado = Label(
            text="Completa los datos del empleado.",
            size_hint_y=None,
            height=190,
            font_size=16,
            halign="left",
            valign="middle",
        )
        contenedor.add_widget(self.resultado)
        return contenedor

    def calcular(self, boton):
        """Lee los campos y llama a la lógica del proyecto."""

        # Borra el resultado anterior antes de calcular.
        self.resultado.text = ""

        try:
            salario = float(self.salario.text.strip())
            vacaciones = int(self.vacaciones.text.strip())

            fecha_ingreso = datetime.strptime(
                self.fecha_ingreso.text.strip(),
                "%Y-%m-%d"
            )

            fecha_retiro = datetime.strptime(
                self.fecha_retiro.text.strip(),
                "%Y-%m-%d"
            )

            # Evita valores especiales como infinito o NaN.
            if not isfinite(salario):
                raise SalarioInvalidoError()

            datos = DatosLiquidacion(
                tipo_retiro=self.tipo_retiro.text,
                salario=salario,
                fecha_ingreso=fecha_ingreso,
                fecha_retiro=fecha_retiro,
                vacaciones_disfrutadas=vacaciones,
            )


            detalle = calcular_detalle_liquidacion(datos)
            total = sumar_conceptos_liquidacion(detalle)

            if not isfinite(total):
                raise OverflowError()

            self.resultado.text = (
                f"Salario pendiente: ${detalle.salario_restante:,.2f}\n"
                f"Prima: ${detalle.prima:,.2f}\n"
                f"Cesantías: ${detalle.cesantias:,.2f}\n"
                f"Intereses de cesantías: ${detalle.intereses:,.2f}\n"
                f"Vacaciones pendientes: ${detalle.vacaciones:,.2f}\n"
                f"Indemnización: ${detalle.indemnizacion:,.2f}\n"
                f"\nTOTAL DE LA LIQUIDACIÓN: ${total:,.2f}"
                        )

        except ValueError:
            self.mostrar_error(
                "Completa todos los campos.\n"
                "Escribe el salario sin separadores de miles,\n"
                "las vacaciones como un número entero\n"
                "y fechas válidas con formato AAAA-MM-DD."
            )

        except (
            SalarioInvalidoError,
            FechaInvalidaError,
            TipoRetiroInvalidoError,
            VacacionesInvalidasError,
        ) as error:
            self.mostrar_error(str(error))

        except OverflowError:
            self.mostrar_error(
                "Los valores ingresados son demasiado grandes.\n"
                "Revísalos e intenta nuevamente."
            )

    def mostrar_error(self, mensaje):
        """Muestra un mensaje amigable en una ventana emergente."""

        contenido = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        etiqueta = Label(
            text=mensaje,
            halign="center",
            valign="middle"
        )
        etiqueta.bind(
            size=etiqueta.setter("text_size")
        )
        contenido.add_widget(etiqueta)

        ventana = Popup(
            title="Revisa los datos",
            content=contenido,
            size_hint=(0.85, 0.5)
        )

        cerrar = Button(
            text="Entendido",
            size_hint_y=None,
            height=45
        )
        cerrar.bind(on_release=ventana.dismiss)
        contenido.add_widget(cerrar)

        ventana.open()

    def limpiar(self, boton):
        """Restablece el formulario para realizar otro cálculo."""
        self.tipo_retiro.text = "Renuncia"
        self.salario.text = ""
        self.fecha_ingreso.text = ""
        self.fecha_retiro.text = ""
        self.vacaciones.text = "0"
        self.resultado.text = "Completa los datos del empleado."
        self.salario.focus = True

      
  