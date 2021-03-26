from django.db import models

# Create your models here.

class Order(models.Model):
    phone = models.CharField(max_length=255, default='')
    data = models.JSONField()
    def handleInput(self, sInput):
        aReturn = []
        sState=self.data["state"]
        if sState=="WELCOMING":
            aReturn.append("Welcome to Wesley's pie shop")
            aReturn.append("Would you like a SMALL, or LARGE?")
            aReturn.append("SMALL is $5, LARGE is $15")
            self.data["state"]="SIZE"
        elif sState=="SIZE":
            self.data["size"]=sInput.lower() 
            if self.data["size"]=="small":
                self.data["price"]=5
            elif self.data["size"]=="large":
                self.data["price"]=15
            else:
                aReturn.append("Oops we only have small and large")
                aReturn.append("Please enter small or large")  
                return aReturn
            aReturn.append("So far your order comes to $" + str(self.data["price"]))      
            aReturn.append("What toppings would you like?")
            aReturn.append("Please enter a list with commas")
            aReturn.append("+$2 per each topping")
            self.data["state"]="TOPPINGS"

        elif sState=="TOPPINGS":
            self.data["toppings"]=sInput.lower()
            nToppings=self.data["toppings"].split(",")
            for x in nToppings:
                self.data["price"]+=2
            aReturn.append("So far your order comes to $" + str(self.data["price"])) 
            aReturn.append("Would you like drinks with that?")
            aReturn.append("Please enter a list with commas or NO")
            aReturn.append("+$2 per each drink")
            self.data["state"]="DRINKS"
        elif sState=="DRINKS":
            if sInput.lower() !="no":
                self.data["drinks"]=sInput.lower()
                nDrinks=self.data["drinks"].split(",")
                for x in nDrinks:
                    self.data["price"]+=2

                
              
            
            aReturn.append("Thank you for your order")
            aReturn.append(self.data["size"]+" pie with "+self.data["toppings"])

            try:
                aReturn.append(self.data["drinks"])
            except:
                pass
            aReturn.append("Please pick up in 20 minutes")
            aReturn.append("The price is $"+str(self.data["price"]))

            self.data["state"]="DONE"
        return aReturn
    def isDone(self):
        if self.data["state"]=="DONE":
            return True
        else:
            return False
    def getState(self):
        return self.data["state"]
    def getSize(self):
        return self.data["size"]
    def getPrice(self):
        return self.data["price"]
    def getToppings(self):
        return self.data["toppings"]
    def getDrinks(self):
        try:
            return self.data["drinks"]    
        except:
            return None
    class Meta:
        # this sets up a SQL index on the phone field
        indexes = [models.Index(fields=['phone'])]
