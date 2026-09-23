from datetime import datetime
import sys
from pathlib import Path

# Agregar src al path
SRC_PATH = Path(__file__).resolve().parents[2]

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

from model.excepciones import (
    FechaInvalidaError,
    SalarioInvalidoError,
    TipoRetiroInvalidoError,
    VacacionesInvalidasError,
)

from model.logica_liquidacion import (
    DESPIDO_CON_JUSTA_CAUSA,
    DESPIDO_SIN_JUSTA_CAUSA,
    RENUNCIA,
    DatosLiquidacion,
    calcular_liquidacion,
)

FORMATO_FECHA = "%Y-%m-%d"


class LiquidacionApp(App):

    def build(self):

        self.title = "Calculadora de Liquidación"

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10,
        )

        titulo = Label(
            text="Calculadora de Liquidación Laboral",
            size_hint=(1, 0.15),
            font_size=22,
        )

        self.tipo_retiro = Spinner(
            text="Seleccione tipo de retiro",
            values=(
                RENUNCIA,
                DESPIDO_CON_JUSTA_CAUSA,
                DESPIDO_SIN_JUSTA_CAUSA,
            ),
            size_hint=(1, 0.1),
        )

        self.salario = TextInput(
            hint_text="Salario mensual",
            multiline=False,
        )

        self.fecha_ingreso = TextInput(
            hint_text="Fecha ingreso (AAAA-MM-DD)",
            multiline=False,
        )

        self.fecha_retiro = TextInput(
            hint_text="Fecha retiro (AAAA-MM-DD)",
            multiline=False,
        )

        self.vacaciones = TextInput(
            hint_text="Vacaciones disfrutadas",
            multiline=False,
        )

        boton = Button(
            text="Calcular Liquidación",
            size_hint=(1, 0.12),
        )

        boton.bind(on_press=self.calcular)

        layout.add_widget(titulo)
        layout.add_widget(self.tipo_retiro)
        layout.add_widget(self.salario)
        layout.add_widget(self.fecha_ingreso)
        layout.add_widget(self.fecha_retiro)
        layout.add_widget(self.vacaciones)
        layout.add_widget(boton)

        return layout

    def mostrar_popup(self, titulo, mensaje):

        popup = Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(0.8, 0.4),
        )

        popup.open()

    def calcular(self, instance):

        try:

            if (
                not self.salario.text.strip()
                or not self.fecha_ingreso.text.strip()
                or not self.fecha_retiro.text.strip()
                or not self.vacaciones.text.strip()
                or self.tipo_retiro.text == "Seleccione tipo de retiro"
            ):
                raise ValueError("Hay campos vacíos")

            

            datos = DatosLiquidacion(
                tipo_retiro=self.tipo_retiro.text,
                salario=float(self.salario.text),
                fecha_ingreso=datetime.strptime(
                    self.fecha_ingreso.text,
                    FORMATO_FECHA,
                ),
                fecha_retiro=datetime.strptime(
                    self.fecha_retiro.text,
                    FORMATO_FECHA,
                ),
                vacaciones_disfrutadas=int(
                    self.vacaciones.text
                ),
            )

            resultado = calcular_liquidacion(datos)

            self.mostrar_popup(
                "Resultado",
                f"Liquidación total:\n${resultado:,.2f}",
            )

        except ValueError as e:

            if str(e) == "Hay campos vacíos":
                self.mostrar_popup(
                    "Campos incompletos",
                    "No puedes dejar campos vacíos.\n\n"
                    "Completa todos los campos y selecciona un tipo de retiro.",
                )
            else:
                self.mostrar_popup(
                    "Error",
                    "Alguno de los valores ingresados tiene un formato incorrecto.\n\n"
                    "Verifica:\n"
                    "- Salario: solo números.\n"
                    "- Fechas: AAAA-MM-DD.\n"
                    "- Vacaciones: número entero.",
                )

        except SalarioInvalidoError as e:
            self.mostrar_popup(
                "Error de salario",
                str(e),
            )

        except FechaInvalidaError as e:
            self.mostrar_popup(
                "Error de fecha",
                str(e),
            )

        except TipoRetiroInvalidoError as e:
            self.mostrar_popup(
                "Error de tipo de retiro",
                str(e),
            )

        except VacacionesInvalidasError as e:
            self.mostrar_popup(
                "Error de vacaciones",
                str(e),
            )


if __name__ == "__main__":
    LiquidacionApp().run()
