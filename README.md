# Proyecto de Liquidación Definitiva

## 👥 Integrantes

- José Manuel Diaz
- Yeisner David Giraldo

## 🔗 Repositorio del equipo

https://github.com/Jose-Dv/liquidacion-definitiva

## 📖 Descripción

Este proyecto consiste en el desarrollo de una calculadora que permite calcular la **liquidación definitiva de un empleado** de acuerdo con el motivo de finalización del contrato.

El programa automatiza el cálculo de las prestaciones sociales, la indemnización cuando corresponda y el valor total de la liquidación, a partir de la información suministrada del empleado.

El objetivo es reducir errores en los cálculos manuales y facilitar la obtención de una liquidación a partir de la información suministrada.

---

## 🗂️ Estructura del proyecto

El proyecto está organizado mediante una separación de responsabilidades entre la lógica de negocio, la interfaz de consola y las pruebas unitarias.

```text
liquidacion-definitiva/
│
├── doc/
│   └── Documentación del proyecto
│
├── src/
│   ├── controller/
│   │   └── __init__.py
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   ├── excepciones.py
│   │   └── logica_liquidacion.py
│   │
│   └── view/
│       ├── gui/
│       │   └── liquidacion_gui.py
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_liquidacion.py
│
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
└── Liquidacion definitiva.xlsx
```

### Responsabilidad de cada componente

| Archivo / Carpeta                 | Responsabilidad                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `src/model/logica_liquidacion.py` | Contiene las constantes y funciones que implementan la lógica de negocio y los cálculos de la liquidación.   |
| `src/model/excepciones.py`        | Contiene las excepciones personalizadas utilizadas para controlar datos inválidos.                           |
| `src/view/main.py`                | Interfaz de consola: solicita los datos al usuario, invoca la lógica y muestra el resultado o los errores.   |
| `src/controller/`                 | Contiene los componentes destinados a coordinar el flujo entre la interfaz y la lógica de negocio.           |
| `tests/test_liquidacion.py`       | Pruebas unitarias utilizando `unittest` para validar los cálculos, validaciones y manejo de errores.         |
| `Liquidacion definitiva.xlsx`     | Tablero de casos de prueba utilizado como apoyo para verificar manualmente los resultados de la liquidación. |
| `src/view/gui/liquidacion_gui.py` | Interfaz gráfica desarrollada con Kivy. Captura los datos, muestra el desglose y presenta mensajes amigables. |
| `main.py`                         | Punto de entrada ubicado en la raíz para ejecutar la interfaz gráfica. |
| `requirements.txt`                | Dependencias necesarias para ejecutar la aplicación en otro computador. |

---

## 🏗️ Arquitectura

El proyecto utiliza una separación por responsabilidades:

### Model

Contiene la lógica de negocio de la aplicación.

`logica_liquidacion.py` contiene funciones independientes para:

* Calcular días trabajados.
* Calcular salario restante.
* Calcular prima.
* Calcular cesantías.
* Calcular intereses sobre las cesantías.
* Calcular vacaciones.
* Calcular indemnización.
* Calcular la liquidación total.

`excepciones.py` contiene las excepciones personalizadas:

* `FechaInvalidaError`
* `SalarioInvalidoError`
* `TipoRetiroInvalidoError`
* `VacacionesInvalidasError`

Las excepciones se mantienen separadas de la lógica de negocio para mejorar la organización y el mantenimiento del código.

### View

`src/view/main.py` contiene la interfaz de consola.

`src/view/gui/liquidacion_gui.py` contiene la interfaz gráfica desarrollada con Kivy.

Ambas interfaces utilizan las funciones de `src/model/logica_liquidacion.py`, por lo que comparten la misma lógica de negocio y no duplican las fórmulas.

### Controller

La carpeta `controller` está destinada a los componentes encargados de coordinar el flujo entre la interfaz y la lógica de negocio.

### Tests

La carpeta `tests` contiene las pruebas unitarias que permiten verificar el comportamiento esperado del sistema.

---

# ▶️ Instalación y ejecución

## Requisitos

Para ejecutar el proyecto se necesita:

- Python 3 instalado.
- Git, si se desea clonar el repositorio.
- Las dependencias incluidas en `requirements.txt`.

## Clonar el repositorio

```bash
git clone https://github.com/Jose-Dv/liquidacion-definitiva.git
cd liquidacion-definitiva
```

Si el repositorio ya está descargado, este paso no es necesario.

## Instalar las dependencias

En Windows:

```bash
py -m pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m pip install -r requirements.txt
```

## Ejecutar la interfaz gráfica

Desde la carpeta raíz del proyecto:

```bash
py main.py
```

La aplicación abrirá una interfaz gráfica desarrollada con Kivy. Esta permite ingresar los datos del empleado, calcular la liquidación, consultar el desglose de los conceptos y limpiar el formulario.

## Ejecutar la interfaz de consola

Desde la carpeta raíz del proyecto:

```bash
py src/view/main.py
```

La consola solicitará el tipo de retiro, salario, fechas y vacaciones disfrutadas.

## Ejecutar las pruebas unitarias

Desde la carpeta raíz del proyecto:

```bash
py -m unittest tests.test_liquidacion -v
```

También se pueden ejecutar mediante descubrimiento automático:

```bash
py -m unittest discover -s tests -p "test_*.py" -v
```

El proyecto contiene 24 pruebas unitarias.

## 🖥️ Generar el ejecutable para Windows

### Prerrequisito

Instalar PyInstaller:

```powershell
py -m pip install -U pyinstaller
```

### Compilación

Desde la carpeta raíz del proyecto, donde se encuentra `main.py`, ejecutar:

```powershell
pyinstaller -F --paths=src main.py
```

El ejecutable se genera en:

```text
dist/main.exe
```

Para ejecutarlo desde PowerShell:

```powershell
.\dist\main.exe
```

También se puede abrir haciendo doble clic sobre `main.exe`.

Las carpetas `build` y `dist` no se almacenan en el repositorio porque contienen archivos generados durante la compilación.

## 📥 Entradas

El usuario debe ingresar la siguiente información a través de `main.py`:

* Tipo de retiro.
* Salario mensual.
* Fecha de ingreso (`AAAA-MM-DD`).
* Fecha de retiro (`AAAA-MM-DD`).
* Días de vacaciones ya disfrutados.

## Tipos de retiro soportados

* `Renuncia`
* `Despido con justa causa`
* `Despido sin justa causa`

En los casos de `Renuncia` y `Despido con justa causa` no se calcula indemnización.

En el caso de `Despido sin justa causa` se calcula la indemnización correspondiente.

---

## ⚙️ Proceso

Una vez ingresada la información, el sistema realiza las siguientes operaciones:

1. **Valida el salario**: debe ser mayor que cero. En caso contrario se genera `SalarioInvalidoError`.

2. **Valida las fechas**: la fecha de retiro no puede ser anterior a la fecha de ingreso. En caso contrario se genera `FechaInvalidaError`.

3. **Valida los días de vacaciones disfrutadas**: no pueden ser negativos. En caso contrario se genera `VacacionesInvalidasError`.

4. **Calcula los días trabajados** entre la fecha de ingreso y la fecha de retiro.

5. **Calcula el salario restante** correspondiente al último período trabajado.

6. **Calcula las prestaciones sociales**:

   * Salario restante.
   * Prima de servicios.
   * Cesantías.
   * Intereses sobre las cesantías.
   * Vacaciones pendientes.

7. **Calcula la indemnización** según el tipo de retiro. La indemnización se genera únicamente para `Despido sin justa causa`.

8. **Valida el tipo de retiro**. Si no corresponde a uno de los tipos soportados, se genera `TipoRetiroInvalidoError`.

9. **Suma todos los conceptos** para obtener el valor total de la liquidación.

10. **Muestra el resultado o el mensaje de error correspondiente** en la interfaz de consola.

---

## 📤 Salidas

El sistema genera como resultado:

* Valor del salario restante.
* Valor de la prima.
* Valor de las cesantías.
* Valor de los intereses sobre las cesantías.
* Valor de las vacaciones pendientes.
* Valor de la indemnización cuando corresponda.
* Valor total de la liquidación.
* Mensajes de error específicos cuando los datos suministrados no son válidos.

---

# 🧪 Casos de prueba

Las pruebas unitarias se encuentran en:

```text
tests/test_liquidacion.py
```

Las pruebas utilizan la biblioteca `unittest` de Python.

Se verifican diferentes componentes de la lógica de liquidación, incluyendo cálculos, validaciones, excepciones y liquidaciones completas.

### Casos normales

Entre los casos probados se encuentran:

* Cálculo de días trabajados.
* Cálculo de salario restante.
* Cálculo de prima.
* Cálculo de cesantías.
* Cálculo de intereses sobre cesantías.
* Cálculo de vacaciones generadas.
* Cálculo de vacaciones disfrutadas.
* Cálculo de vacaciones pendientes.
* Cálculo de indemnización.
* Cálculo de días de indemnización.
* Cálculo de indemnización según el tipo de retiro.
* Liquidación completa por renuncia.
* Liquidación completa por despido sin justa causa.
* Suma de los conceptos de liquidación.

### Casos de error

Las pruebas también verifican:

* Salario negativo → `SalarioInvalidoError`.
* Salario igual a cero → `SalarioInvalidoError`.
* Fecha de retiro anterior a la fecha de ingreso → `FechaInvalidaError`.
* Días de vacaciones disfrutadas negativos → `VacacionesInvalidasError`.
* Tipo de retiro no soportado → `TipoRetiroInvalidoError`.

Para ejecutar las pruebas:

```bash
python -m unittest tests.test_liquidacion -v
```

---

# 📊 Casos de prueba en Excel

Además de las pruebas unitarias en Python, el proyecto incluye un archivo de Excel utilizado como apoyo para la verificación manual de los cálculos:

```text
Liquidacion definitiva.xlsx
```

El archivo permite comparar diferentes escenarios de liquidación y verificar visualmente los resultados obtenidos.

### Casos normales

Se contemplan escenarios como:

* Despido con justa causa.
* Renuncia voluntaria.
* Despido sin justa causa.

En estos escenarios se verifican los diferentes conceptos que componen la liquidación y la aplicación de la indemnización según corresponda.

### Casos excepcionales

Se contemplan escenarios con diferentes condiciones de entrada, como:

* Salario alto.
* Salario bajo.
* Vacaciones agotadas.
* Diferentes condiciones para los intereses de cesantías.

Estos casos permiten comprobar el comportamiento del sistema ante valores que se encuentran fuera de los escenarios habituales.

### Casos de error

Se contemplan casos como:

* Salario en cero.
* Salario negativo.
* Fecha de retiro anterior a la fecha de ingreso.
* Días de vacaciones negativos.
* Datos inválidos.

El objetivo es verificar que el sistema rechace los datos incorrectos y genere el error correspondiente en lugar de producir una liquidación incorrecta.

---

# 🛠️ Tecnologías utilizadas

* **Python 3.12**
* **unittest** — pruebas unitarias.
* **Microsoft Excel** — tablero de verificación manual de casos de prueba.
* **Visual Studio Code** — entorno de desarrollo.

---

# 🧹 Principios de calidad de código

El proyecto busca aplicar principios de **Clean Code** y buenas prácticas de desarrollo:

* Funciones pequeñas y con una responsabilidad específica.
* Nombres descriptivos.
* Separación de responsabilidades.
* Constantes para valores utilizados en los cálculos.
* Excepciones personalizadas.
* Separación de excepciones y lógica de negocio.
* Separación entre modelo, vista, controlador y pruebas.
* Evitar duplicación de código.
* Documentación mediante docstrings.
* Código orientado a facilitar el mantenimiento y las pruebas.

---

# 👥 Integrantes

| Nombre       | GitHub                                           |
| ------------ | ------------------------------------------------ |
| Jhoan Ríos   | [@jhoan-rios](https://github.com/jhoan-rios)     |
| Andrés Rosas | [@andres-rosas](https://github.com/andres-rosas) |

---

# 📌 Estado del proyecto

Proyecto desarrollado como parte de las prácticas de programación, con evolución progresiva de la estructura, arquitectura, pruebas unitarias y calidad del código.

La versión actual incorpora una separación de responsabilidades entre la lógica de negocio, las excepciones, la interfaz de consola y las pruebas unitarias.
