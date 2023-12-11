class StringField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, f"_{self.name}", None)

    def __set__(self, instance, value):
        if not isinstance(value, str): 
            raise TypeError(f"Field '{self.name}' must be a string")
        setattr(instance, f"_{self.name}", value)
        
class ModelCreator(type):
    def __new__(cls, name, bases, attrs): 
        fields = {name: attr for name, attr in attrs.items() if isinstance(attr, StringField)}

        for field_name, field in fields.items():
            field.__set_name__(None, field_name)
        
        old_init = attrs['__init__']

        def __init__(self, *args, **kwargs):
            
            kwargs_list = list(kwargs.items()) # заговнокодил, виноват, но зато работает! :)
    
            for field_name, value in kwargs_list: #
                if field_name in fields: #
                    setattr(self, field_name, value) #
                    del kwargs[field_name] #
        
            old_init(self, *args, **kwargs) #
        
        attrs['__init__'] = __init__
    
        return super().__new__(cls, name, bases, attrs)
    
class Student(metaclass=ModelCreator):
    name = StringField()
    mother_name = StringField()
    vather_name = StringField()
    
    age = 18
    
    def __init__(self, school):
        self.school = school

s = Student(name="Jee", mother_name="Kio", vather_name="Holoho", school="YorkyUni")
print(vars(s))