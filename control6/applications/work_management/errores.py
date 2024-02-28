class CampoRequeridoError(Exception):
    def __init__(self, campo, status_code=400):
        self.campo = campo
        self.status_code = status_code
        self.message = f'El campo {campo} es obligatorio.'
        super().__init__(self.message)

class NoTienSiguienteEstado(Exception):
    def __init__(self, status_code=400):
        self.status_code = status_code
        self.message = f'No tiene siguiente estado.'
        super().__init__(self.message)