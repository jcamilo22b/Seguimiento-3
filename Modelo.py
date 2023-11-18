from PyQt5.QtGui import QImage
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut
import numpy as np

class DicomModel:
    def __init__(self, path):
        self.dicom = pydicom.dcmread(path)
        self.path = path

    def apply_modality_lut(self):
        ds = self.dicom
        imagen = apply_modality_lut(ds.pixel_array, ds)

        if imagen.dtype != np.uint8:
            imagen = (np.maximum(imagen, 0) / imagen.max()) * 255.0
            imagen = np.uint8(imagen)

        return QImage(imagen, imagen.shape[1], imagen.shape[0], QImage.Format_Grayscale8)

    def get_patient_info(self):
        ds = self.dicom
        return f'{ds.PatientName}', f'{ds.PatientID}', f'{ds.PatientSex}', f'{ds.PatientWeight}', f'{ds.Modality}'
