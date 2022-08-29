
class Elements:
    def __init__(self, default_value='unknown'):
        self.or_city = default_value
        self.dst_city = default_value
        self.str_date = default_value
        self.end_date = default_value
        self.budget = default_value

    @property
    def elements(self):
        return {
        'or_city': self.or_city,
        'dst_city':self.dst_city,
        'str_date' : self.str_date,
        'end_date' : self.end_date,
        'budget' : self.budget,
        }
       
    def is_complete(self):
        return 'unknown' not in self.elements.values()

    def next_unknown_element(self):
        """
        Return the first attribute with 'unknown' value.
        """
        unknown = [key for key, value in self.elements.items() if value == 'unknown']
        return unknown[0] if unknown else None
        
    def reset_values(self):
        return self.__init__()



