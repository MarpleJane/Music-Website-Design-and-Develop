#coding: utf-8


def cached_property(func):
    """http://code.activestate.com/recipes/576563-cached-property/"""
    def get(self):
        try:
            return self._property_cache[func]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[func] = func(self)
            return x
        except KeyError:
            x = self._property_cache[func] = f(self)
            return x
    return property(get)


def get_obj_attrs(attrs, obj):
    return {attr: getattr(obj, attr) for attr in attrs}


def get_attrs(attrs, obj_list):
    return [{attr: getattr(obj, attr) for attr in attrs} for obj in obj_list]
