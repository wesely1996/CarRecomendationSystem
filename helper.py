class Car:
    
    def __init__(self):
        """
        # Initialize a Car object with default values.
        """
        self.state = None
        self.brand = None
        self.model = None
        self.year = None
        self.distanceTraveled = None
        self.bodyType = None
        self.fuelType = None
        self.cubicCapacity = None
        self.motorStrength = None
        self.fixedPrice = False
        self.exchange = False
        self.linkToArticle = None
        self.numberOfDoors = None
        self.numberOfSeats = None
        self.color = None
        self.condition = None
        self.price = None

    def __init__(self, brand=None, model=None, year=None, distanceTraveled=None, bodyType=None, fuelType=None, cubicCapacity=None, 
            motorStrength=None, fixedPrice=False, exchange=False, linkToArticle=None, numberOfDoors=None, numberOfSeats=None, 
            color=None, condition=None, price=None, state=None):
        """
        Initialize a Car object with given values.
        """
        self.state = state
        self.brand = brand
        self.model = model
        self.year = year
        self.distanceTraveled = distanceTraveled
        self.bodyType = bodyType
        self.fuelType = fuelType
        self.cubicCapacity = cubicCapacity
        self.motorStrength = motorStrength
        self.fixedPrice = fixedPrice
        self.exchange = exchange
        self.linkToArticle = linkToArticle
        self.numberOfDoors = numberOfDoors
        self.numberOfSeats = numberOfSeats
        self.color = color
        self.condition = condition
        self.price = price

    def toString(self):
        return f'Car[state={self.state}, brand={self.brand}, model={self.model}, year={self.year}, distanceTraveled={self.distanceTraveled}, bodyType={self.bodyType}, fuelType={self.fuelType}, cubicCapacity={self.cubicCapacity}, motorStrength={self.motorStrength}, fixedPrice={self.fixedPrice}, exchange={self.exchange}, linkToArticle={self.linkToArticle}, numberOfDoors={self.numberOfDoors}, numberOfSeats={self.numberOfSeats}, color={self.color}, condition={self.condition}, price={self.price}]'
    