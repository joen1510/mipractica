class Ciudad:
    def __init__(self, fecha):
        self.fecha=fecha

    def toDBCollection(self):
        return{
            'Fecha': self.fecha
        }