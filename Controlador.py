import sys
from PyQt5.QtWidgets import QApplication
from Modelo import *
from Vista import *

class DicomController:
    def __init__(self, main_window, dicom_viewer):
        self.main_window = main_window
        self.dicom_viewer = dicom_viewer

    def run(self):
        self.main_window.show()
        
    def show_dicom_viewer(self):
        self.main_window.hide()  #Hide the login screen
        self.dicom_viewer.show()  #Show the DICOM viewer screen

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    dicom_viewer = DicomViewerUI()
    dicom_controller = DicomController(main_window, dicom_viewer)

    main_window.set_dicom_viewer(dicom_viewer)
    main_window.set_controller(dicom_controller)
    dicom_controller.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()