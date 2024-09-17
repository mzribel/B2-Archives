import itertools

from packages.PEx2.person import Person

class Contact(Person):
    iter_counter = itertools.count()

    # --- CONSTRUCTEUR --- #
    def __init__(self, lastname:str="", firstname:str="", phone_number="", email="", **kwargs):
        super().__init__(lastname, firstname, kwargs.get("dob"), kwargs.get("age"))
        self.id:int = next(Contact.iter_counter)
        self.phone_number = phone_number
        self.email = email
    # ------------------- #

    # --- METHODES --- #
    def __str__(self):
        final_string = super().__str__()
        if self.phone_number:
            final_string += f"\n   Phone number: {self.phone_number}"
        if self.email:
            final_string += f"\n   Email: {self.email}"
        return final_string

    def display(self):
        print(self.__str__())