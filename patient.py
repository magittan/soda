class patient():

    def __init__(self, ID, name = "John Doe", **kwargs):
        self.ID = ID
        self.name = name
        self.age = kwargs['age']
        self.sex = kwargs['sex']

class hospital():

    def __init__(self, ID, **kwargs):
        self.ID = ID
        self.name
        self.address
        self.city
        self.zipcode

    def determineLatLong(self):
