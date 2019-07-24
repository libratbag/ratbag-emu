'''
Helper class to interact only with the absolute value of a number
'''
class Absolute(object):
    _multiplier = 0
    _abs = 0

    def __init__(self, n):
        self.__set__(self, n)

    def __set__(self, instance, n):
        self._multiplier = n and 1 if n > 0 else -1
        self._abs = abs(n)

    def __int__(self):
        return self._multiplier * self._abs

    def __float__(self):
        return self._multiplier * self._abs

    def __str__(self):
        return str(self.__int__())

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return self._abs

    def __add__(self, other):
        return max(0, self._multiplier * (self._abs + abs(other)))

    def __iadd__(self, other):
        self._abs = max(0, self._abs + other)
        return self

    def __sub__(self, other):
        return max(0, self._multiplier * (self._abs - abs(other)))

    def __isub__(self, other):
        self._abs = max(0, self._abs - other)
        return self

    def __mul__(self, other):
        return self._abs * abs(other)

    def __imul__(self, other):
        self._abs *= abs(other)
        return self

    def __truediv__(self, other):
        return self._multiplier * abs(self.__int__() / other)

    def __itruediv__(self, other):
        self._abs /= abs(other)
        return self


class AbsInt(Absolute):
    def __init__(self, n):
        super().__init__(int(n))


class AbsFloat(Absolute):
    def __init__(self, n):
        super().__init__(float(n))
