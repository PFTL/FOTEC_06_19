from persons import Person, Learner


class Student(Person):
    def __init__(self, name, last_name, age, course):
        super().__init__(name, last_name, age)
        self.course = course
        self.enrolled = False

    def enroll(self):
        self.enrolled = True

    def is_enrolled(self):
        if self.enrolled:
            print('Is enrolled')
        else:
            print('Not enrolled')


me = Student('Aquiles', 'Carattino', 33, 'Python for the Lab')
print(me.get_full_name())
print(me.course)
# me.enroll()
me.is_enrolled()
