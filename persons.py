class Person:
    def __init__(self, name, last_name, age=None):
        self.name = name
        self.last_name = last_name
        self.age = age

    def get_full_name(self):
        return self.name + ' ' + self.last_name

    def calculate_birth_year(self):
        if self.age is None:
            print('Age not defined')
            return
        else:
            return 2019-self.age


class Learner:
    def __init__(self, interest):
        self.interest = interest


if __name__ == '__main__':
    me = Person('Aquiles', 'Carattino')
    you = Person('José', "Van 't Hoof", 30)

    print(me.name)
    print(me.last_name)
    print('Birth year: ', me.calculate_birth_year())
    me_full_name = me.get_full_name()
    print(me_full_name)

    print(you.name)
    print(you.last_name)
    print(you.calculate_birth_year())
