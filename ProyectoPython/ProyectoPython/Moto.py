class Moto:
    # Class variables
    # Variables de clase
    headings = ['ID', 'Marca', 'Modelo', 'Año', 'Kilometraje']
    fields = {
        '-id-': 'ID de la Moto:',
        '-brand-': 'Marca de la Moto:',
        '-model-': 'Modelo de la Moto:',
        '-year-': 'Año:',
        '-mileage-': 'Kilometraje:',
        '-pos_file-': 'Posición en el Archivo'
    }

    # Constructor method
    # Método del constructor
    def __init__(self, id, brand, model, year, mileage, pos_file, erased=False):
        # Instance attributes
        # Atributos de instancia
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage
        self.pos_file = pos_file
        self.erased = erased

    # Equality comparison method
    # Método de comparación de igualdad
    def __eq__(self, other):
        return other.pos_file == self.pos_file

    # String representation method
    # Método de representación en cadena
    def __str__(self):
        return (
            str(self.id) + str(self.brand) + str(self.model) +
            str(self.year) + str(self.mileage) + str(self.pos_file)
        )

    # Method to check if the moto is in a specific position
    # Método para verificar si la moto está en una posición específica
    def moto_in_pos(self, pos):
        return self.pos_file == pos

    # Method to set moto attributes
    # Método para establecer atributos de la moto
    def set_moto(self, brand, model, year, mileage):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = mileage