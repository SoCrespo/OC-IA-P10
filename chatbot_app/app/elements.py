
from dataclasses import dataclass, fields

@dataclass 
class Elements:
    or_city: str = 'unknown'
    dst_city: str = 'unknown'
    str_date: str = 'unknown'
    end_date: str = 'unknown'
    budget: str = 'unknown'
    
    def is_complete(self):
        return all([item != 'unknown' for item in fields(self)])