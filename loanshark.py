class LoanShark:
    def __init__(self, name, rate, stars,link,lat,long,photo_ref):
        self.name = name # vendor name
        self.rate = rate # vendor interest rate
        self.stars = stars # vendor star rating
        self.link = link # vendor website link
        self.lat = lat # vendor latitude
        self.long = long # vendor longitude
        self.photo_ref = photo_ref # google photo reference of vendor

    def getName(self):
        return self.name

    def getRate(self):
        return self.rate

    def getStars(self):
        return self.stars

    def getLink(self):
        return self.link

    def getLat(self):
        return self.lat

    def getLong(self):
        return self.long
    def getPhotoReference(self):
        return self.photo_ref


