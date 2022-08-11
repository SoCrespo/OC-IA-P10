
class Elements:
    def __init__(self, default_value='unknown'):
        self.or_city = default_value
        self.dst_city = default_value
        self.str_date = default_value
        self.end_date = default_value
        self.budget = default_value

    @property
    def elements(self):
        return self.or_city, self.dst_city, self.str_date, self.end_date, self.budget

    def is_complete(self):
        return 'unknown' not in self.elements
        
    def reset_values(self):
        return self.__init__()


