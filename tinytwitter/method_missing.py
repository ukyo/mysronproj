#coding: utf8

class MethodMissing(object):
    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            def method(*args, **kw):
                return self.method_missing(name, *args, **kw)
            return method
    
    def method_missing(self, name, *args, **kw):
        raise AttributeError, name
