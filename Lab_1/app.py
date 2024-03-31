import xml.etree.ElementTree as ET
import json
import dicttoxml
import re

class Person:
    def __init__(self, name, middlename, familyname, age, course):
        self.name = name
        self.middlename = middlename
        self.familyname = familyname
        self.age = age
        self.course = course
        

    def asDict(self):
        data = {
            "Name": self.name,
            "MiddleName": self.middlename,
            "FamilyName": self.familyname,
            "Age": self.age,
            "Course": self.course
        }
        return data


class Driver:
    def Save(self, p, f):
        pass
        
    def Load(self, f):
        pass

    def Find(self, p, name, familyname):
        pass

    def Delete(self, p, name, familyname):
        pass


class XMLDriver(Driver):
    def Save(self, p, f):
        xmlData = {'Persons': []}

        for person in p:
            xmlData['Persons'].append(person.asDict())
            
        xmlString = dicttoxml.dicttoxml(xmlData,return_bytes=False)
        print(xmlData)

        with open(f, "w") as my_file:
            my_file.write(xmlString)

    def Load(self, f):
        tree = ET.parse(f)
        root = tree.getroot()

        p = []

        for person_data in root:
            name = person_data.find('Name').text
            middlename = person_data.find('MiddleName').text
            familyname = person_data.find('FamilyName').text
            age = int(person_data.find('Age').text)
            course = int(person_data.find('Course').text)
            p.append(Person(name, middlename, familyname, age, course))
                
        return p

    def Find(self, p, name, familyname):
        found_persons = []

        for person in p:
            if person.name == name and person.familyname == familyname:
                found_persons.append(person)

        return found_persons

    def Delete(self, p, name, familyname):
        updated_persons = []

        for person in p:
            if person.name != name or person.familyname != familyname:
                updated_persons.append(person)

        return updated_persons


class JSONDriver(Driver):
    def Save(self, p, f):
        jsonData = []

        for person in p:
            jsonData.append(person.asDict())
            
        print(jsonData)

        with open(f, "w") as my_file:
            json.dump(jsonData, my_file)

    def Load(self, f):
        with open(f, "r") as my_file:
            jsonData = json.load(my_file)

            p = []

            for person_data in jsonData:
                name = person_data['Name']
                middlename = person_data['MiddleName']
                familyname = person_data['FamilyName']
                age = int(person_data['Age'])
                course = int(person_data['Course'])
                p.append(Person(name, middlename, familyname, age, course))
                
            return p

    def Find(self, p, name, familyname):
        found_persons = []

        for person in p:
            if person.name == name and person.familyname == familyname:
                found_persons.append(person)

        return found_persons

    def Delete(self, p, name, familyname):
        p = [person for person in p if not (person.name == name and person.familyname == familyname)]
        return p


class PersonHandler:
    def __init__(self):
        self.p = []

    def SavePersons(self, d, f):
        d.Save(self.p, f)

    def LoadPersons(self, d, f):
        self.p = d.Load(f)
        
    ## ВАЛИДАЦИЯ
        
    def validate_name(self, name):
        pattern = r"^[A-ZА-Я][a-zа-яЁё]{1,19}$"
        return bool(re.match(pattern, name))

    def validate_middlename(self, middlename):
        pattern = r"^[A-ZА-Я][a-zа-яЁё]{1,19}$"
        return bool(re.match(pattern, middlename))

    def validate_familyname(self, familyname):
        pattern = r"^[A-ZА-Я][a-zа-яЁё]{1,19}$"
        return bool(re.match(pattern, familyname))
    
    def validate_age(self, age):
        return 18 <= age <= 35

    def validate_course(self, course):
        return 1 <= course <= 5

    def AddPerson(self, name, middlename, familyname, age, course): 
        if (self.validate_name(name) and 
            self.validate_middlename(middlename) and 
            self.validate_familyname(familyname) and 
            self.validate_age(age) and 
            self.validate_course(course)):
            self.p.append(Person(name, middlename, familyname, age, course))
            print("Студент успешно добавлен.")
        else:
            print("Некорректные данные студента.")

        #self.p.append(Person(name, middlename, familyname, age, course))

    def FindPerson(self, driver, name, familyname):
        found_persons = driver.Find(self.p, name, familyname)

        if len(found_persons) > 0:
            for person in found_persons:
                print(f"Имя: {person.name}")
                print(f"Отчество: {person.middlename}")
                print(f"Фамилия: {person.familyname}")
                print(f"Возраст: {person.age}")
                print(f"Курс: {person.course}")
                print()
        else:
            print("Студент не найден.")

    def DeletePerson(self, driver, name, familyname):
        self.p = driver.Delete(self.p, name, familyname)
        print("Студент удален.")


class Program:
    @staticmethod
    def SaveXML(handler, f):
        driver = XMLDriver()
        handler.SavePersons(driver, xml_filename)
        print("Данные сохранены в формате XML.")

    @staticmethod
    def SaveJSON(handler, f):
        driver = JSONDriver()
        handler.SavePersons(driver, json_filename)
        print("Данные сохранены в формате JSON.")
        

    @staticmethod
    def AddPerson(handler):
        name = input("Введите имя студента: ")
        middlename = input("Введите отчество студента: ")
        familyname = input("Введите фамилию студента: ")
        age = int(input("Введите возраст студента: "))
        course = int(input("Введите курс студента: "))
        handler.AddPerson(name, middlename, familyname, age, course)

    @staticmethod
    def FindPerson(handler, format):
        name = input("Введите имя студента: ")
        familyname = input("Введите фамилию студента: ")
        if format == "xml":
            driver = XMLDriver()
            handler.FindPerson(driver, name, familyname)
        elif format == "json":
            driver = JSONDriver()
            handler.FindPerson(driver, name, familyname)
        else:
            print("Студент не найден.")

    @staticmethod
    def DeletePerson(handler, format):
        name = input("Введите имя студента: ")
        familyname = input("Введите фамилию студента: ")
        if format == "xml":
            driver = XMLDriver()
            handler.DeletePerson(driver, name, familyname)
            Program.SaveXML(handler, "persons.xml")
        elif format == "json":
            driver = JSONDriver()
            handler.DeletePerson(driver, name, familyname)
            Program.SaveJSON(handler, "persons.json")
        else:
            print("Ошибка.")

    @staticmethod
    def Do(xml_filename, json_filename):
        handler = PersonHandler()
        
        while True:
            print("1. Добавить студента")
            print("2. Сохранить студента в формате JSON")
            print("3. Сохранить студента в формате XML")
            print("4. Найти студента")
            print("5. Удалить студента")
            print("6. Выход")
            
            choice = input("Выберите действие: ")
            if choice == "1":
                Program.AddPerson(handler)
            elif choice == "2":
                Program.SaveJSON(handler, json_filename)
            elif choice == "3":
                Program.SaveXML(handler, xml_filename)
            elif choice == "4":
                format = input("Введите формат: (xml/json): ")
                Program.FindPerson(handler, format)
            elif choice == "5":
                format = input("Введите формат: (xml/json): ")
                Program.DeletePerson(handler, format)
            elif choice == "6":
                break  
            else:
                print("Ошибка ввода. Попробуйте снова.")

if __name__ == '__main__':
    xml_filename = "persons.xml"  
    json_filename = "persons.json" 
    Program.Do(xml_filename, json_filename)
