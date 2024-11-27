from pyswip import Prolog

class FamilyChatbot:
    def __init__(self, prolog_file):
        self.prolog = Prolog()
        self.prolog.consult(prolog_file)

    def _extract_names(self, statement, relationship):
        parts = statement.split(relationship)
        name1 = parts[0].strip().lower().capitalize()
        name2 = parts[1].strip().lower().capitalize()
        return name1, name2

    def check_fact(self, fact):
        try:
            query = f"\\+ ({fact})" 
            contradiction = list(self.prolog.query(query))
            if contradiction:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error Checking fact:") 
    def check_sex(self, name, sex):
        if sex=='male':
            sex='female'
        elif sex=='female':
            sex='male'
        query = f"{sex}({name.lower()})"
        contradiction = self.check_fact(query)
        if contradiction: return True
        return False

    def check_relation(self, name1, name2):
        query = f"related({name1.lower()}, {name2.lower()})"
        contradiction = self.check_fact(query)
        if contradiction: return True
        return False
    
    def children_check(self,children, parent):
        for child in children:
            if self.check_relation(child, parent):
                return True
        return False
    def process_statement(self, statement):
        if "is a male" in statement:
            name = statement.replace("is a male", "").strip().lower().capitalize()
            if self.check_sex(name,'male'):
                print("That’s impossible!")
            else:
                try:
                    self.prolog.assertz(f"male({name.lower()})")
                    print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a female" in statement:
            name = statement.replace("is a female", "").strip().lower().capitalize()
            if self.check_sex(name, "female"):
                print("That’s impossible!")
            else:
                try:
                    self.prolog.assertz(f"female({name.lower()})")
                    print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is the father of" in statement:
            parent, child = self._extract_names(statement, "is the father of")
            if self.check_relation(child,parent) or self.check_sex(parent, 'male'):
                print("That’s impossible!")
            else:
                try:
                    if parent.lower() == child.lower() :
                        print(f"That’s impossible! A person can't be their own father.")
                    else: 
                        self.prolog.assertz(f"male({parent.lower()})")
                        self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is the mother of" in statement:
            parent, child = self._extract_names(statement, "is the mother of")
            if self.check_relation(child,parent) or self.check_sex(parent, 'female'):
                print("That's impossible!")
            else:
                try:
                    if parent.lower() == child.lower() :
                        print(f"That’s impossible! A person can't be their own mother.")
                    else:
                        self.prolog.assertz(f"female({parent.lower()})")
                        self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is a brother of" in statement:
            sibling1, sibling2 = self._extract_names(statement, "is a brother of")
            if self.check_sex(sibling1,'male') or self.check_relation(sibling2,sibling1):
                print("That’s impossible!")
            else:
                try:
                    if sibling1.lower == sibling2.lower:
                        print(f"That’s impossible! A person can't be their own brother.")
                    else:
                        self.prolog.assertz(f"male({sibling1.lower()})")
                        self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                        self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is a sister of" in statement:
            sibling1, sibling2 = self._extract_names(statement, "is a sister of")
            if self.check_sex(sibling1,'female') or self.check_relation(sibling2,sibling1):
                print("That’s impossible!")
            else:
                try:
                    if sibling1.lower == sibling2.lower:
                        print(f"That’s impossible! A person can't be their own sister.")
                    else:
                        self.prolog.assertz(f"female({sibling1.lower()})")
                        self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                        self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")

        elif "is a grandmother of" in statement:
            grandparent, grandchild = self._extract_names(statement, "is a grandmother of")
            if self.check_sex(grandparent,'female') or self.check_relation(grandchild,grandparent):
                print("That’s impossible!")
            else:
                try:
                    if grandparent.lower() == grandchild.lower():
                        print(f"That’s impossible! A person can't be their own grandmother.")
                    else:
                        self.prolog.assertz(f"female({grandparent.lower()})")
                        self.prolog.assertz(f"grandparent({grandparent.lower()}, {grandchild.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")

        elif "is a grandfather of" in statement:
            grandparent, grandchild = self._extract_names(statement, "is a grandfather of")
            if self.check_sex(grandparent,'male') or self.check_relation(grandchild,grandparent):
                print("That’s impossible!")
            else:
                try:
                    if grandparent.lower() == grandchild.lower():
                        print(f"That’s impossible! A person can't be their own grandfather.")
                    else:
                        self.prolog.assertz(f"male({grandparent.lower()})")
                        self.prolog.assertz(f"grandparent({grandparent.lower()}, {grandchild.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is a grandson of" in statement:
            grandchild, grandparent = self._extract_names(statement, "is a grandson of")
            if self.check_sex(grandchild,'male') or self.check_relation(grandparent,grandchild):
                print("That's impossible! A person can't be their own grandson.")
            else:
                try:
                    if grandchild.lower() == grandparent.lower():
                        print(f"That’s impossible! A person can't be their own grandson.")
                    else:
                        self.prolog.assertz(f"male({grandchild.lower()})")
                        self.prolog.assertz(f"grandchild({grandparent.lower()}, {grandparent.lower()})")
                        print("OK!, I learned that something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a granddaughter of" in statement:
            grandchild, grandparent = self._extract_names(statement, "is a granddaughter of")
            if self.check_sex(grandchild,'female') or self.check_relation(grandparent,grandchild):
                    print(f"That’s impossible!")
            else:
                try:
                    if grandchild.lower() == grandparent.lower():
                        print(f"That’s impossible! A person can't be their own granddaughter.")
                    else:
                        self.prolog.assertz(f"female({grandchild.lower()})")
                        self.prolog.assertz(f"grandchild({grandparent.lower()}, {grandparent.lower()})")
                        print("OK!, I learned that something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a son of" in statement:
            child, parent = self._extract_names(statement, "is a son of")
            if self.check_sex(child,'male') or self.check_relation(parent,child):
                    print(f"That’s impossible!")
            else:
                try:
                    if child.lower() == parent.lower():
                        print(f"That’s impossible! A person can't be their own son.")
                    else:
                        self.prolog.assertz(f"male({child.lower()})")
                        self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a daughter of" in statement:
            child, parent = self._extract_names(statement, "is a daughter of")
            if self.check_sex(child,'female') or self.check_relation(parent,child):
                    print(f"That’s impossible!")
            else:
                try:
                    if child.lower() == parent.lower():
                        print(f"That’s impossible! A person can't be their own daughter.")
                    else:
                        self.prolog.assertz(f"female({child.lower()})")
                        self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is an aunt of" in statement:
            aunt, niece_or_nephew = self._extract_names(statement, "is an aunt of")
            if self.check_sex(aunt,'feale') or self.check_relation(niece_or_nephew,aunt):
                print(f"That’s impossible! ")
            else:
                try:
                    if aunt.lower() == niece_or_nephew.lower():
                        print(f"That’s impossible! A person can't be their own aunt.")
                    else:
                        self.prolog.assertz(f"female({aunt.lower()})")
                        self.prolog.assertz(f"pibling({aunt.lower()}, {niece_or_nephew.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is an uncle of" in statement:
            uncle, niece_or_nephew = self._extract_names(statement, "is an uncle of")
            if self.check_sex(uncle,'male') or self.check_relation(niece_or_nephew,uncle):
                print(f"That’s impossible! ")
            else:
                try:
                    if uncle.lower() == niece_or_nephew.lower():
                        print(f"That’s impossible! A person can't be their own uncle.")
                    else:
                        self.prolog.assertz(f"male({uncle.lower()})")
                        self.prolog.assertz(f"pibling({uncle.lower()}, {niece_or_nephew.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a niece of" in statement:
            niece, aunt_or_uncle = self._extract_names(statement, "is a niece of")
            if self.check_sex(niece,'female') or self.check_relation(niece,aunt_or_uncle):
                print(f"That’s impossible! ")
            else:
                try:
                    if niece.lower() == aunt_or_uncle.lower():
                        print(f"That’s impossible! A person can't be their own niece.")
                    else:
                        self.prolog.assertz(f"female({niece.lower()})")
                        self.prolog.assertz(f"nibling({niece.lower()}, {aunt_or_uncle.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "is a nephew of" in statement:
            nephew, aunt_or_uncle = self._extract_names(statement, "is a nephew of")
            if self.check_sex(nephew,'male') or self.check_relation(nephew,aunt_or_uncle):
                print(f"That’s impossible!")
            else:
                try:
                    if nephew.lower() == aunt_or_uncle.lower():
                        print(f"That’s impossible! A person can't be their own nephew.")
                    else:
                        self.prolog.assertz(f"male({nephew.lower()})")
                        self.prolog.assertz(f"nibling({nephew.lower()}, {aunt_or_uncle.lower()})")
                        print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "are siblings" in statement:
            sibling1, sibling2 = self._extract_names(statement.replace(" are siblings", ""), " and ")
            if self.check_relation(sibling2, sibling1):
                print("That’s impossible!")
            else:
                try:
                    self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                    self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                    print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "are the parents of" in statement:
            parent1, parent2, child = statement.replace("are the parents", "").replace("of","and").split("and")
            if self.check_relation(child, parent1) or self.check_relation(child, parent2):
                print("That’s impossible!")
            else:
                try:
                    self.prolog.assertz(f"parent({parent1.lower()}, {child.lower()})")
                    self.prolog.assertz(f"parent({parent2.lower()}, {child.lower()})")
                    print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible!")
        elif "is a child of" in statement:
            child, parent = self._extract_names(statement, "is a child of")
            if self.check_relation(parent, child):
                print("That’s impossible!")
            else:
                try:
                    self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                    print("OK! I learned something.")
                except Exception as e:
                    print(f"That’s impossible! ")
        elif "are the children of" in statement:
            parts = statement.replace("are the children", "").replace("of", "and").replace(", "," and ").split("and")
            children = [child.strip().lower().capitalize() for child in parts[:-1]]
            parent = parts[-1].strip().lower().capitalize()
            if self.children_check(children, parent):
                print("That’s impossible!")
            else:
                if len(parts) >= 2:
                    try:
                        for child in children:
                            self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                        print("OK! I learned something.")
                    except Exception as e:
                        print(f"That’s impossible!")
                else:
                    print("Invalid statement. Please follow the sentence patterns.")
        else:
            print("Invalid statement. Please follow the sentence patterns.")


    
    def process_question(self, question):

        if "Is" in question and "the father of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            parent, child = self._extract_names(modified_question, "the father of")
            result = list(self.prolog.query(f"father({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "the brother of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            person1, person2 = self._extract_names(modified_question, "the brother of")
            result = list(self.prolog.query(f"brother({person1.lower()}, {person2.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "the sister of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            person1, person2 = self._extract_names(modified_question, "the sister of")
            result = list(self.prolog.query(f"sister({person1.lower()}, {person2.lower()})"))
            print("Yes!" if result else "No!")

        elif "Who is the father of" in question:
            child = question.replace("Who is the father of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"father(X, {child.lower()})"))
            if results:
                print(f"The father of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the father of {child} is.")

        elif "Are" in question and "siblings" in question:
            parts = question.replace("Are", "").replace("siblings", "").replace("?", "").split("and")
            if len(parts) == 2:
                person1 = parts[0].strip().lower().capitalize()
                person2 = parts[1].strip().lower().capitalize()
                result = list(self.prolog.query(f"sibling({person1}, {person2})"))
                print("Yes!" if result else "No!")
            else:
                print("Invalid question. Please follow the sentence patterns.")

        elif "Are" in question and "the parents of" in question:
            modified_question = question.replace("Are", "").replace("the parents of", "").replace("?", "").strip()
            parts = modified_question.rsplit("and", 1)
            if len(parts) == 2:
                parent_part = parts[0].strip()
                rest = parts[1].strip().split()
                parent1 = parent_part.strip()
                parent2 = rest[0].strip()
                child = " ".join(rest[1:]).strip()
                result1 = list(self.prolog.query(f"parent({parent1.lower()}, {child.lower()})"))
                result2 = list(self.prolog.query(f"parent({parent2.lower()}, {child.lower()})"))
                if result1 and result2:  
                    print("Yes!")
                else:
                    print("No!")
            else:
                print("Invalid question. Please follow the sentence patterns.")

        elif "Is" in question and "the mother of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            parent, child = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"mother({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")

        elif "Who is the mother of" in question:
            child = question.replace("Who is the mother of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"mother(X, {child.lower()})"))
            if results:
                print(f"The mother of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the mother of {child} is.")

        elif "Who are the siblings of" in question:
            person = question.replace("Who are the siblings of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"sibling(X, {person.lower()})"))
            if results:
                siblings = [result['X'].capitalize() for result in results]
                print(f"The siblings of {person} are: {', '.join(siblings)}")
            else:
                print(f"I don’t know the siblings of {person}.")

        elif "Who are the brothers of" in question:
            person = question.replace("Who are the brothers of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"brother(X, {person.lower()})"))
            if results:
                brothers = [result['X'].capitalize() for result in results]
                print(f"The brothers of {person} are: {', '.join(brothers)}")
            else:
                print(f"I don’t know the brothers of {person}.")

        elif "Who are the sisters of" in question:
            person = question.replace("Who are the sisters of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"sister(X, {person.lower()})"))
            if results:
                sisters = [result['X'].capitalize() for result in results]
                print(f"The sisters of {person} are: {', '.join(sisters)}")
            else:
                print(f"I don’t know the sisters of {person}.")

        elif "Who are the grandparents of" in question:
            grandchild = question.replace("Who are the grandparents of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"grandparent(X, {grandchild.lower()})"))
            if results:
                grandparents = [result['X'].capitalize() for result in results]
                print(f"The grandparents of {grandchild} are: {', '.join(grandparents)}")
            else:
                print(f"I don’t know the grandparents of {grandchild}.")

        elif "Who are the grandchildren of" in question:
            grandparent = question.replace("Who are the grandchildren of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"grandchild(X, {grandparent.lower()})"))
            if results:
                grandchildren = [result['X'].capitalize() for result in results]
                print(f"The grandchildren of {grandparent} are: {', '.join(grandchildren)}")
            else:
                print(f"I don’t know the grandchildren of {grandparent}.")
                
        elif "What is the relationship between" in question:
            parts = question.replace("What is the relationship between", "").replace("?", "").split("and")
            if len(parts) == 2:
                person1 = parts[0].strip().lower().capitalize()
                person2 = parts[1].strip().lower().capitalize()
                results = list(self.prolog.query(f"relationship({person1}, {person2}, R)"))
                if results:
                    print(f"The relationship between {person1} and {person2} is: {' and '.join(relationships)}.")
                else:
                    print(f"I don’t know the relationship between {person1} and {person2}.")
            else:
                print("Invalid question. Please follow the sentence patterns.")

        elif "Who are the sons of" in question:
            parent = question.replace("Who are the sons of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"son(X, {parent.lower()})"))
            if results:
                children = [result['X'].capitalize() for result in results]
                print(f"The sons of {parent} are: {', '.join(children)}")
            else:
                print(f"I don’t know the sons of {parent}.")
        elif "Who are the daughters of" in question:
            parent = question.replace("Who are the daughters of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"daughter(X, {parent.lower()})"))
            if results:
                children = [result['X'].capitalize() for result in results]
                print(f"The daughters of {parent} are: {', '.join(children)}")
            else:
                print(f"I don’t know the daughters of {parent}.")

        elif "Is" in question and "a daughter of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            child, parent = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"daugther({child.lower()}, {parent.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "a son of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            child, parent = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"son({child.lower()}, {parent.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "a child of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            child, parent = self._extract_names(modified_question, "a child of")
            result = list(self.prolog.query(f"parent({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")
        
        elif "Is" in question and "an uncle of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            uncle, niece_or_nephew = self._extract_names(modified_question, "an uncle of")
            result = list(self.prolog.query(f"uncle({uncle.lower()}, {niece_or_nephew.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "an aunt of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            aunt, niece_or_nephew = self._extract_names(modified_question, "an aunt of")
            result = list(self.prolog.query(f"aunt({aunt.lower()}, {niece_or_nephew.lower()})"))
            print("Yes!" if result else "No!")
        
        elif "Is" in question and "a niece of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            niece, aunt_or_uncle = self._extract_names(modified_question, "a niece of")
            result = list(self.prolog.query(f"niece({niece.lower()}, {aunt_or_uncle.lower()})"))
            print("Yes!" if result else "No!")
        elif "Who are the parents of" in question:
            child = question.replace("Who are the parents of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"parent(X, {child.lower()})"))
            if results:
                parents = [result['X'].capitalize() for result in results]
                print(f"The parents of {child} are: {', '.join(parents)}.")
            else:
                print(f"I don’t know the parents of {child}.")
        elif "Is" in question and "a grandson of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            grandchild, grandparent = self._extract_names(modified_question, "a grandson of")
            result = list(self.prolog.query(f"grandson({grandchild.lower()}, {grandparent.lower()})"))
            print("Yes!" if result else "No!")

        elif "Is" in question and "a grandaughter of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            grandchild, grandparent = self._extract_names(modified_question, "a granddaughter of")
            result = list(self.prolog.query(f"granddaughter({grandchild.lower()}, {grandparent.lower()})"))
            print("Yes!" if result else "No!")
        
        elif "Is" in question and "a grandfather of" in question: 
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            grandparent, grandchild = self._extract_names(modified_question, "a grandfather of")
            result = list(self.prolog.query(f"grandfather({grandparent.lower()}, {grandchild.lower()})"))
            print("Yes!" if result else "No!")
        elif "Is" in question and "a grandmother of" in question: 
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            grandparent, grandchild = self._extract_names(modified_question, "a grandmother of")
            result = list(self.prolog.query(f"grandmother({grandparent.lower()}, {grandchild.lower()})"))
            print("Yes!" if result else "No!")
        elif "Is" in question and "a nephew of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            nephew, aunt_or_uncle = self._extract_names(modified_question, "a nephew of")
            result = list(self.prolog.query(f"nephew({nephew.lower()}, {aunt_or_uncle.lower()})"))
            print("Yes!" if result else "No!")

        elif "Who are the children of" in question:
            parent = question.replace("Who are the children of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"parent({parent.lower()}, X)"))
            if results:
                children = [result['X'].capitalize() for result in results]
                print(f"The children of {parent} are: {', '.join(children)}.")
            else:
                print(f"I don’t know the children of {parent}.")

        elif "Are" in question and "the children of" in question:
            parts = question.replace("Are", "").replace("of","and").replace("the children", "").replace("?", "").replace(",","and").split("and")
            print(parts)
            if len(parts) >= 2:
                children = [child.strip().lower().capitalize() for child in parts[:-1]]
                parent = parts[-1].strip().lower().capitalize()
                results = [
                    list(self.prolog.query(f"parent({parent.lower()}, {child.lower()})"))
                    for child in children
                ]
                if all(results):
                    print("Yes!")
                else:
                    print("No!")
            else:
                print("Invalid question. Please follow the sentence patterns.")

        elif "Are" in question and "related" in question:
            parts = question.replace("Are", "").replace("related", "").replace("?", "").split("and")
            if len(parts) == 2:
                person1 = parts[0].strip().lower().capitalize()
                person2 = parts[1].strip().lower().capitalize()
                if self.check_relation(person1, person2):
                    print("Yes!")
                else:
                    print("No!")
            else:
                print("Invalid question. Please follow the sentence patterns.")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def statements(self):
        print("Here are the commands you can use:")
        print("Statements:")
        print("  - [Name] is a male")
        print("  - [Name] is a female")
        print("  - [Name] is the father of [Name]")
        print("  - [Name] is the mother of [Name]")
        print("  - [Name] is a brother of [Name]")
        print("  - [Name] is a sister of [Name]")
        print("  - [Name] is a grandmother of [Name]")
        print("  - [Name] is a grandfather of [Name]")
        print("  - [Name] is a grandson of [Name]")
        print("  - [Name] is a granddaughter of [Name]")
        print("  - [Name] is a son of [Name]")
        print("  - [Name] is a daughter of [Name]")
        print("  - [Name] is an aunt of [Name]")
        print("  - [Name] is an uncle of [Name]")
        print("  - [Name] is a niece of [Name]")
        print("  - [Name] is a nephew of [Name]")
        print("  - [Name] and [Name] are siblings")
        print("  - [Name] is a child of [Name]")
        print("  - [Name] and [Name] are the parents of [Name]")
        print("  - [Name], [Name] and [Name]... are the children of [Name]")
        print("Type 'quit' or 'exit' to end the chat.")

    
    def questions(self):
        print("Here are the commands you can use:")
        print("Questions:")
        print("  - Is [Name] the father of [Name]?")
        print("  - Is [Name] the mother of [Name]?")
        print("  - Is [Name] the brother of [Name]?")
        print("  - Is [Name] the sister of [Name]?")
        print("  - Who is the father of [Name]?")
        print("  - Who is the mother of [Name]?")
        print("  - Who are the siblings of [Name]?")
        print("  - Who are the brothers of [Name]?")
        print("  - Who are the sisters of [Name]?")
        print("  - Who are the grandparents of [Name]?")
        print("  - Who are the grandchildren of [Name]?")
        print("  - What is the relationship between [Name] and [Name]?")
        print("  - Who are the sons of [Name]?")
        print("  - Who are the daughters of [Name]?")
        print("  - Is [Name] a son of [Name]?")
        print("  - Is [Name] a daughter of [Name]?")
        print("  - Is [Name] a child of [Name]?")
        print("  - Is [Name] an uncle of [Name]?")
        print("  - Is [Name] an aunt of [Name]?")
        print("  - Is [Name] a niece of [Name]?")
        print("  - Is [Name] a nephew of [Name]?")
        print("  - Is [Name] an grandfather of [Name]?")
        print("  - Is [Name] an grandmother of [Name]?")
        print("  - Is [Name] a grandson of [Name]?")
        print("  - Is [Name] a grandaughter of [Name]?")
        print("  - Who are the children of [Name]?")
        print("  - Who are the parents of [Name]?")
        print("  - Are [Name], [Name] and [Name]... the children of [Name]?")
        print("  - Are [Name] and [Name] related?")
        print("Type 'quit' or 'exit' to end the chat.")
    def chat(self):
        print("Welcome to the Family Relationship Chatbot!")
        print("You can tell me statements or ask me questions about family relationships.")
        print("Statements or statement to see the available statements. And Questions or questions to see the available questions.")
        print("Type 'quit' or 'exit' to end the chat.")
        while True:
            user_input = input("\n> ").strip()
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            elif user_input.lower() in ["statements", "statement"]:
                self.statements()
            elif user_input.lower() in ["questions", "question"]:
                self.questions()
            elif "?" in user_input:
                self.process_question(user_input)
            else:
                self.process_statement(user_input)

if __name__ == "__main__":
    chatbot = FamilyChatbot("kb.pl")
    chatbot.chat()
