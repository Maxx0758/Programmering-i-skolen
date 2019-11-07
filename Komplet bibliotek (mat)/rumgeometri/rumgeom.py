import math
import numpy as np

class Point():
    def __init__(self, coords: list()):
        self.coords = coords


class Vector():
    def __init__(self, coords: list()):
        self.coords = coords

    @classmethod
    def connect(cls, x1, y1, z1, x2, y2, z2, t1 = 0, t2 = 0):
        '''
        Returns a new vector from two points.
        '''
        return cls(x2 - x1, y2 - y1, z2 - z1, t2 - t1)


    @classmethod
    def fromPoint(cls, p: Point):
        '''
        Returns a new vector from a point
        '''
        return cls(p.coords)


    def __add__(self, other):
        if len(other.coords) != len(self.coords):
            raise ValueError("Wrong fucking length, nøøb")
        v = Vector(list())
        for a, b in zip(self.coords, other.coords):
            v.coords.append(a+b)
        return v


    def __mul__(self, other):
        if len(self.coords) != len(other.coords):
            raise ValueError("Vectors are not the same fucking length, nøøb")
        d = 0
        for i in range(len(self.coords)):
            d += self.coords[i] * other.coords[i]
        return d


    def length(self) -> float: # TODO make more efficient
        l = 0
        for c in self.coords:
            l += math.sqrt(c**2)
        return l


    def __str__(self):
        s = "(" + ("{}," for i in range(len(self.coords))) + ")".format(c for c in self.coords)
        return s


class Line():
    def __init__(self, p0, d):
        self.p0 = p0
        self.d = d

    '''
    Factory methods
    '''
    @classmethod
    def createNew(cls, x0, y0, z0, a, b, c):
        '''
        Creates a new Line from a point and a direction vector
        '''
        p0 = Vector(x0, y0, z0)
        d = Vector(a, b, c)
        return cls(p0, d)


    @classmethod
    def createTwoPoints(cls, x1, y1, z1, x2, y2, z2):
        '''
        Creaates a new Line from two points on the line
        '''
        d = Vector(x2 - x1, y2 - y1, z2 - z1)
        p0 = Vector(x1, y1, z1)
        return cls(p0, d)


    def point(self, t: (float, int) = 0) -> Point:
        '''
        Return a point on the line, from a given parameter
        '''
        if not isinstance(t, (float, int)):
            raise TypeError('Parameter is not a valid number')
        p = Vector.fromPoint(self.p0)
        s = scale(t, self.d)
        return add(p, s)


    def getXPoint(self, x):
        '''
        Returns a point on the line, with the given x-getZCoord
        '''
        #Find the correct parameter
        t = (x-self.p0.x) / self.d.x
        return self.point(t)


    def __str__(self):
        return "(x, y, z) = ({}, {}, {}) + t*({}, {}, {})".format(self.p0.x, self.p0.y, self.p0.z, self.d.x, self.d.y, self.d.z)

class Plane():
    '''
    The class describes a plane in space.

    It is created by a point and two direction vectors
    or by three points.

    Attributes
    ----------
    p0 : Vector(x, y, z), where (x, y, z) is a point on the Plane
    d1 : A direction vector for the plane.
    d2 : Another direction vector for the plane. Can not be parallel to d1

    Factory methods
    -------
    createNew(x0, y0, z0, a1, b1, c1, a2, b2, c2)
        Returns a plane through (x0, y0, z0) with
        the direction vectors (a1, b1, c1)^T and (a2, b2, c2)^T

    createThreePoints(x1, y1, z1, x2, y2, z2, x3, y3, z3)
        Returns a plane through the three points
        (x1, y1, z1), (x2, y2, z2) and (x3, y3, z3)


    normal()
        Returns a normal vector to the plane.
        The normal will be a unit vector.
    '''


    def __init__(self, p0, d1, d2):
        self.p0 = p0
        self.d1 = d1
        self.d2 = d2

    '''
    Factory methods
    '''
    @classmethod
    def createNew(cls, x0, y0, z0, a1, b1, c1, a2, b2, c2):
        '''
        Creates a new Plane from a point and two direction vectors
        '''
        p0 = Point(x0, y0, z0)
        d1 = Vector(a1, b1, c1)
        d2 = Vector(a2, b2, c2)
        return cls(p0, d1, d2)


    @classmethod
    def createThreePoints(cls, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        '''
        Creaates a new Line from two points on the line
        '''
        d = np.array([x2 - x1, y2 - y1, z2 - z1])
        p0 = np.array([x1, y1, z1])
        return cls(p0, d)


    def normal(self) -> Vector:
        '''
        Returns a normal unit vector to the plane
        by crossing the two direction vectors
        '''
        return normalize(cross(self.d1, self.d2))


    def isInPlane(self, p) -> bool:
        '''
        Returns True if the point is in the plane,
        and False otherwise.
        '''
        #Testing for zero is done with math.isclose, to avoid rounding/floating point errors.
        #Since we are testing near zero, abs_tol is set to 1e-09
        return math.isclose(math.fabs(dot(self.normal(), Vector.connect(p.x, p.y, p.z, self.p0.x, self.p0.y, self.p0.z))),0, rel_tol=1e-09, abs_tol=1e-09)


    def listZPoints(self, ts, ss):
        Z = []
        for t in ts:
            for s in ss:
                Z.append(self.point(t, s).z)
        return Z


    def getZCoord(self, x, y):
        '''
        Returnerer en z-koordinat i planen, givet x og y.
        '''
        n = self.normal()
        z = (-n.x*(x - self.p0.x) - n.y*(y - self.p0.y) + n.z*self.p0.z) / n.z
        return z


    def point(self, t: (float, int) = 0, s: (float, int) = 0) -> Vector:
        '''
        Returns a point on the plane, from two given parameters
        '''
        p = Vector.fromPoint(self.p0)
        s1 = scale(t, self.d1)
        s2 = scale(s, self.d2)
        return add(add(p, s1), s2)


    def __str__(self):
        return "(x, y, z) = ({}, {}, {}) + t*({}, {}, {}) + s*({}, {}, {})".format(self.p0.x, self.p0.y, self.p0.z, self.d1.x, self.d1.y, self.d1.z, self.d2.x, self.d2.y, self.d2.z)


def scale(s: (float, int), v: Vector) -> Vector:
    '''
    Returns a copy of v, scaled by s.
    '''
    coords = list()
    res = Vector(coords)
    for i in range(len(v.coords)):
        res.coords[i] *= s
    return res


def normalize(v: Vector) -> Vector: # Function is fucked TODO
    '''
    Returns a unit-vector in the direction v
    '''
    if v.length() > 0.000001:
        s = 1 / v.length()
        return scale(s,v)
    else:
        return Vector(list([0 for i in range(len(v.coords))]))


def cross(v1: Vector, v2: Vector) -> Vector: # Function is fucked TODO
    '''
    Returns the cross product of v1 and v2
    '''
    if len(v1.coords) != 3 or len(v2.coords) != 3:
        raise ValueError("Vectors have to be 3 fucking D, nøøb")
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x
    return Vector(x, y, z)


def angle(v1: Vector, v2: Vector) -> float:
    '''
    Returns the angle in degrees between v1 and v2
    '''
    return math.degrees(math.acos((v1 * v2) / (v1.length() * v2.length())))


def distancePointPlane(p: Point, a: Plane) -> float:
    #The distance between the point and the plane is
    # the absolute value of the dot product between
    # the unit normal vector of the plane, and the projection
    # of a vector connecting the point to the plane, onto that unit
    # normal vectors
    return math.fabs((a.normal() * Vector.connect(p.x, p.y, p.z, a.p0.x, a.p0.y, a.p0.z)))


def intersect(l: Line, p: Plane) -> Point:
    '''
    Calculates the intersection between a Line and a Plane.
    Returns None if the two arguments are parallel.
    '''
    if math.isclose((l.d * p.normal()), 0):
        #If the line direction is perpendicular to the plane normal,
        # the line and plane must be parallel.
        return None
    else:
        #There exists a parameter t, which makes
        # p.isInPlane(l.point(t)) == 0
        #Let's find it.
        #Initial guess
        t1 = 1
        p1 = l.point(t1)
        d1 = distancePointPlane(p1, p)
        t2 = 2
        p2 = l.point(t2)
        d2 = distancePointPlane(p2, p)

        #Calculate line through the two points (t,d)
        a = (d2 - d1) / (t2 - t1)
        b = d1 - a * t1

        #Find the t-value where d is zero
        # 0 = at+b <=> t = -b/a
        t = -b / a
        print('parameter: {}'.format(t))
        return l.point(t)


class Matrix():
    '''
    The class describes a matrix in space.

    It is created by a list of vectors.
    All vectors have 4 elements. (4D)

    Attributes
    ----------
    vectors : list(Vector(x, y, z, t), Vector(x, y, z, t), Vector(x, y, z, t), Vector(x, y, z, t)), where (x, y, z, t) is a point on the Plane
    m : The length of the matrix. The amount of vectors in the list of vectors

    Magic methods
    -------
    

    Factory methods
    -------
    equal_size(other)
        returns true, if one the self matrix is of equal size as the other matrix.
    '''


    def __init__(self, vectors: list()): # List of vectors
        prev = None
        for v in vectors:
            if prev == None:
                continue
            if len(v.coords) != len(prev.coords):
                raise ValueError("Vectors are not same fucking length, nøøb")
            prev = v
        
        self.vectors = vectors
        
        self.m = len(self.vectors)
        self.n = len(self.vectors.coords)


    def __add__(self, other):
        if not self.equal_size(other):
            raise ValueError("Wrong fucking size, nøøb")
        
        vectors = list()
        for i in range(self.m):
            v1 = self.vectors[i]
            v2 = other.vectors[i]
            vectors.insert(i, v1 + v2)
        return Matrix(vectors)


    def __mul__(self, other):
        if isinstance(other, Vector):
            # Matrix vector product
            v = Vector(list())
            for i in range(len(other.vectors)):
                v += scale(other.vectors[i][i], self.vectors[i])
            # v1 = scale(other.x, self.vectors[0])
            # v2 = scale(other.y, self.vectors[1])
            # v3 = scale(other.z, self.vectors[2])
            # v4 = scale(other.t, self.vectors[3])
            return v

        elif isinstance(other, Matrix):
            # Matrix matrix product
            if self.m != other.n:
                raise ValueError("Wrong fucking sizes, nøøb")

            selfVectors = self.vectors
            otherVectors = other.vectors

            # vo1 = otherVectors[0].coords[1] # Other matrix; vector 1, coordinate 2

            #v1 = scale(other.vectors[0].x, self.vectors[0]) + scale(other.vectors[0].y, self.vectors[1]) + scale(other.vectors[0].z, self.vectors[2]) + scale(other.vectors[0].t, self.vectors[3])
            #v2 = scale(other.vectors[1].x, self.vectors[0]) + scale(other.vectors[1].y, self.vectors[1]) + scale(other.vectors[1].z, self.vectors[2]) + scale(other.vectors[1].t, self.vectors[3])
            #v3 = scale(other.vectors[2].x, self.vectors[0]) + scale(other.vectors[2].y, self.vectors[1]) + scale(other.vectors[2].z, self.vectors[2]) + scale(other.vectors[2].t, self.vectors[3])
            #v4 = scale(other.vectors[3].x, self.vectors[0]) + scale(other.vectors[3].y, self.vectors[1]) + scale(other.vectors[3].z, self.vectors[2]) + scale(other.vectors[3].t, self.vectors[3])
            l = 0
            vectors = list()
            for k in range(self.m):
                for i in range(self.m):
                    for j in range(other.n):
                        l += selfVectors[j].coords[i] * otherVectors[k].coords[j] 
                        cordinator = []
                        cordinator.append(l)
                    v = Vector(cordinator)
                vectors.append(v)
            return Matrix(vectors)

        else:
            raise ValueError("Wrong fucking type, nøøb")


    @classmethod
    def identity_matrix(cls):
        # Generates the identity matrix; Static
        v1 = Vector(1, 0, 0, 0)
        v2 = Vector(0, 1, 0, 0)
        v3 = Vector(0, 0, 1, 0)
        v4 = Vector(0, 0, 0, 1)
        return Matrix([v1, v2, v3, v4])


    def transpose(self):
        vectors = list()
        for i in range(self.n):
            v = Vector(list())
            for j in range(self.m):
                v.append(self.vectors[n].coords[m])
            vectors.insert(i, v)
        return Matrix(vectors)


    def equal_size(self, other):
        return other.m == self.m


    def get_rotation_matrix(self, angleX, angleY, angleZ):
        v1 = Vector(math.cos(angleZ)*math.cos(angleY), math.sin(angleZ)*math.cos(angleY), -1*math.sin(angleY))
        v2 = Vector(math.cos(angleZ)*math.sin(angleY)*math.sin(angleX)-math.sin(angleZ)*math.cos(angleX), math.sin(angleZ)*math.sin(angleY)*math.sin(angleX)+math.cos(angleZ)*math.cos(angleX), math.cos(angleY)*math.sin(angleX))
        v3 = Vector(math.cos(angleZ)*math.sin(angleY)*math.cos(angleX)+math.sin(angleZ)*math.sin(angleX), math.sin(angleZ)*math.sin(angleY)*math.cos(angleX)-math.cos(angleZ)*math.sin(angleX), math.cos(angleY)*math.cos(angleX))

        return Matrix([v1, v2, v3])