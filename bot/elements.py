
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

    def summarize(self) -> str:
        """
        Return a summary of the attributes if all are known.
        """
        if self.is_complete():
            return (
                f"You want to fly from {self.or_city} to {self.dst_city}, "
                f"departing on {self.str_date} and coming back on {self.end_date}, "
                f"with a budget of {self.budget}."
                ) 
        else:
            return "I don't have enough information to summarize your request."

    def reset_values(self):
        return self.__init__()



