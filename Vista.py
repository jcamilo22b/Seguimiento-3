from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from pathlib import Path
import os
from Modelo import *

class DicomViewerUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_folder_path = ''
        self.current_images = []
        self.current_index = 0
        self.ui = loadUi('SliderInfo.ui', self)
        self.initUI()

    def initUI(self):
        self.ui.pushButton.clicked.connect(self.loadFolder)
        self.ui.horizontalSlider.valueChanged.connect(self.updateImage)

    def loadFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta')
        if folder_path:
            self.current_folder_path = folder_path
            self.loadImages()
            self.ui.horizontalSlider.setMaximum(len(self.current_images) - 1)
            self.updateImage()

    def loadImages(self):
        self.current_images = [str(file) for file in Path(self.current_folder_path).rglob('*.dcm')]

    def updateImage(self):
        if not self.current_images:
            return

        self.current_index = self.ui.horizontalSlider.value()
        image_path = self.current_images[self.current_index]

        dicom_model = DicomModel(image_path)
        dicom_image = dicom_model.apply_modality_lut()

        pixmap = QPixmap.fromImage(dicom_image)
        self.ui.label.setPixmap(pixmap)

        _, archivo = os.path.split(image_path)
        self.ui.Fileprueba.setText(archivo)

        info1, info2, info3, info4, info5 = dicom_model.get_patient_info()
        self.ui.Fileprueba_2.setText(info1)
        self.ui.Fileprueba_3.setText(info2)
        self.ui.Fileprueba_4.setText(info3)
        self.ui.Fileprueba_5.setText(info4)
        self.ui.Fileprueba_6.setText(info5)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("login.ui", self)

        self.ingresar.clicked.connect(self.mostrar_datos)
        self.dicom_viewer = None
        self.controller = None

    def set_dicom_viewer(self, dicom_viewer):
        self.dicom_viewer = dicom_viewer

    def set_controller(self, controller):
        self.controller = controller

    def mostrar_datos(self):
        usuario = self.line_user.text()
        contrasena = self.line_password.text()

        if usuario == "medicoAnalista" and contrasena == "bio12345":
            self.mostrar_mensaje_bienvenide()
            self.controller.show_dicom_viewer()
        else:
            self.mostrar_mensaje_error()

    def mostrar_mensaje_error(self):
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Warning)
        mensaje.setWindowTitle("Error de autenticación")
        mensaje.setText("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        mensaje.exec_()

    def mostrar_mensaje_bienvenide(self):
        mensajebienvenide = QMessageBox()
        mensajebienvenide.setIcon(QMessageBox.Information)
        mensajebienvenide.setWindowTitle('Bienvenide :)')
        mensajebienvenide.setText('Inicio de sesión válido.')
        mensajebienvenide.exec_()