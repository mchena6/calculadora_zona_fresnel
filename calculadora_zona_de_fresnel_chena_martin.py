import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def convertir_float(input_str: str) -> float:
    # Manejar "," y "."
    cleaned = input_str.replace(',', '.')

    # Convertir input a float
    try:
        val = float(cleaned)
        if val <= 0:
            raise ValueError("El valor debe ser mayor a cero")
        return val
    except ValueError: 
        raise ValueError("Formato numérico inválido")


def truncar_decimales(number: float) -> str:
    # Convertir numero a string y truncar la parte decimal
    str_num = str(number)
    entero, decimal = str_num.split('.')
    return f"{entero}.{decimal[:2]}"


def calcular_zona_fresnel(d_total: float, frecuencia: float) -> float:
    # Fórmula de la imagen: F1 = 8.656 * sqrt(D / f)
    return 8.656 * math.sqrt(d_total / frecuencia)


class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.inciar_interfaz()

    def inciar_interfaz(self):
        self.setWindowTitle("Calculadora - Zona de Fresnel")
        self.setFixedSize(450, 520)

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Titulo
        title_label = QLabel("Primera Zona de Fresnel")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Subtitulo
        subtitle_label = QLabel("Ingrese los parámetros en las unidades indicadas.\nSe aceptan puntos y comas decimales.")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(subtitle_label)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Inputs de datos (distancia y frecuencia)
        self.input_d = self.crear_inputs("Distancia Total del Enlace (D) [km]:")
        self.input_f = self.crear_inputs("Frecuencia de Operación (f) [GHz]:")

        # Agregar inputs al layout principal
        layout.addLayout(self.input_d['layout'])
        layout.addLayout(self.input_f['layout'])

        # Boton de Calcular
        self.btn_calculate = QPushButton("Calcular Zona de Fresnel")
        self.btn_calculate.setFixedHeight(40)
        self.btn_calculate.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
            QPushButton:pressed {
                background-color: #003E66;
            }
        """)
        self.btn_calculate.clicked.connect(self.calcular)
        layout.addWidget(self.btn_calculate)

        # Resultados
        self.result_box = QFrame()
        self.result_box.setStyleSheet("""
            QFrame {
                background-color: #F0F4F8;
                border: 1px solid #D0D7DE;
                border-radius: 8px;
            }
        """)
        result_layout = QVBoxLayout(self.result_box)
        result_layout.setContentsMargins(15, 15, 15, 15)

        # Mostrar distancia total
        self.lbl_distance = QLabel("Distancia Total: -- km")
        self.lbl_distance.setStyleSheet("color: #333; font-size: 13px;")

        # Mostrar resultado (r1)
        self.lbl_result = QLabel("Radio Zona de Fresnel (r): -- m")
        lbl_res_font = QFont("Arial", 13)
        lbl_res_font.setBold(True)
        self.lbl_result.setFont(lbl_res_font)
        self.lbl_result.setStyleSheet("color: #007ACC;")

        # Agregar resultado al Layout principal
        result_layout.addWidget(self.lbl_distance)
        result_layout.addWidget(self.lbl_result)

        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def crear_inputs(self, label_text: str) -> dict:
        # Campos de entrada
        v_layout = QVBoxLayout()
        v_layout.setSpacing(4)

        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #333;")

        # Estilo al editar campo
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Ej: 2.5 o 2,5")
        line_edit.setFixedHeight(32)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #CCC;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
        """)

        v_layout.addWidget(label)
        v_layout.addWidget(line_edit)

        return {'layout': v_layout, 'edit': line_edit}

    def calcular(self):
        try:
            # Obtener valores de los campos
            d_str = self.input_d['edit'].text()
            f_str = self.input_f['edit'].text()

            # Validar que los campos no esten vacios
            if not d_str or not f_str:
                raise ValueError("Todos los campos son obligatorios.")

            # Conversion de valores
            d_total = convertir_float(d_str)
            frecuencia = convertir_float(f_str)

            # Calculo de zona de fresnel
            r_metros = calcular_zona_fresnel(d_total, frecuencia)
            r_truncado = truncar_decimales(r_metros)

            # Actualizar la interfaz con los resultados
            self.lbl_distance.setText(f"Distancia Total: {d_total:.2f} km")
            self.lbl_result.setText(f"Radio Zona de Fresnel (r): {r_truncado} m")

        except ValueError as err:
            # Ventana emergente en caso de error de entrada
            QMessageBox.critical(
                self, 
                "Error de Entrada", 
                f"Por favor revise los datos ingresados:\n\n• {str(err)}",
                QMessageBox.StandardButton.Ok
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculadora()
    window.show()
    sys.exit(app.exec())