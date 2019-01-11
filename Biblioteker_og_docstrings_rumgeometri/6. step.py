import math

class Point():
    '''
    Repræsenterer et punkt i rummet
    '''

    def __init__(self, x, y, z):
        '''
        Retunerer et punkt
        '''
        self.x = x
        self.y = y
        self.z = z


class Vector():
    '''
    Repræsenterer en vector i rummet
    '''    
    def __init__(self, x, y, z):
        '''
        Returnerer en vector
        '''
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def stedvektor(cls, p: Point):
        '''
        Retunerer en stedvektor til et punkt.
        '''
        return cls(p.x, p.y, p.z)
    
    @classmethod    
    def forbindende_vektor(cls, x1, y1, z1, x2, y2, z2):
        '''
        Retunerer en forbindende vektor.                                                                
        '''
        return cls(x2 - x1, y2 - y1, z2 - z1)
    
    @classmethod # statisk metode som gør at man kan skrive vector.classens navn (vector, da classen hedder "vector")
    def sumvektor(cls, v1, v2):
        '''
        Tager summen af to vektorer.
        '''
        return cls(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
    
    @classmethod
    def differens(cls, v1, v2):
        '''
        Tager differensen af to vektorer.
        '''
        return cls(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
    
    
    def length(self):
        '''
        Retunerer længden af vektoren, hvor man har en vektor som input. Altså ikke længden mellem to punkter.
        '''
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    

    def __str__(self):
        '''
        Laver formatet vektorer udskrives på.
        '''
        return "({}, {}, {})".format(self.x, self.y, self.z)        


p1 = Point(1, 2, 3)
p = Vector.stedvektor(p1)
#print("Stedvektoren er {}.".format(p))

v = Vector.forbindende_vektor(1, 2, 3, 4, 5, 6)
#print("Den forbindende vektor er {}.".format(v))

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

s = Vector.sumvektor(v1, v2)
#print("Summen af vektorerne {} & {} er {}".format(v1, v2, s))

d = Vector.differens(v1, v2)
#print("Differensen af vektorerne {} & {} er {}".format(v1, v2, d))

l = v1.length()
print("Længden af vektoren er {}".format(l))

# Udkommenterer dette, da det er forstyrrende, når vi kører det
'''
print(Point.__doc__)  # Printer docstringen lige efter class Point():
print(Point.__init__.__doc__) # Printer docstringen lige efter __init__(self, x, y, z): under class Point():
print(Vector.__doc__)
print(Vector.__init__.__doc__)
print(Vector.stedvektor.__doc__)
print(Vector.__str__.__doc__)
nemt = True
if nemt == True:
    print("fucking nemt mand")
'''