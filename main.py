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

    def _assert_fact(self, fact):
        try:
            query = f"\\+ ({fact})" 
            contradiction = list(self.prolog.query(query))
            if contradiction:
                print("That’s impossible!")
            else:
                self.prolog.assertz(fact)
                print("OK! I learned something.")
        except Exception as e:
            print(f"Error asserting fact: {e}")

    def process_statement(self, statement):
        if "is a male" in statement:
            name = statement.replace("is a male", "").strip().lower().capitalize()
            try:
                self.prolog.assertz(f"male({name.lower()})")
                print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is a female" in statement:
            name = statement.replace("is a female", "").strip().lower().capitalize()
            try:
                self.prolog.assertz(f"female({name.lower()})")
                print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is the father of" in statement:
            parent, child = self._extract_names(statement, "is the father of")
            try:
                if parent.lower() == child.lower() :
                    print(f"That’s impossible! A person can't be their own father.")
                else: 
                    self.prolog.assertz(f"male({parent.lower()})")
                    self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is the mother of" in statement:
            parent, child = self._extract_names(statement, "is the mother of")
            try:
                if parent.lower() == child.lower() :
                    print(f"That’s impossible! A person can't be their own mother.")
                else:
                    self.prolog.assertz(f"female({parent.lower()})")
                    self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is a brother of" in statement:
            sibling1, sibling2 = self._extract_names(statement, "is a brother of")
            try:
                if sibling1.lower == sibling2.lower:
                    print(f"That’s impossible! A person can't be their own brother.")
                else:
                    self.prolog.assertz(f"male({sibling1.lower()})")
                    self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                    self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is a sister of" in statement:
            sibling1, sibling2 = self._extract_names(statement, "is a sister of")
            try:
                if sibling1.lower == sibling2.lower:
                     print(f"That’s impossible! A person can't be their own sister.")
                else:
                    self.prolog.assertz(f"female({sibling1.lower()})")
                    self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                    self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")

        elif "is a grandmother of" in statement:
            grandparent, grandchild = self._extract_names(statement, "is a grandmother of")
            try:
                if grandparent.lower() == grandchild.lower():
                    print(f"That’s impossible! A person can't be their own grandmother.")
                else:
                    self.prolog.assertz(f"female({grandparent.lower()})")
                    self.prolog.assertz(f"grandparent({grandparent.lower()}, {grandchild.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")

        elif "is a grandfather of" in statement:
            grandparent, grandchild = self._extract_names(statement, "is a grandfather of")
            try:
                if grandparent.lower() == grandchild.lower():
                    print(f"That’s impossible! A person can't be their own grandfather.")
                else:
                    self.prolog.assertz(f"male({grandparent.lower()})")
                    self.prolog.assertz(f"grandparent({grandparent.lower()}, {grandchild.lower()})")
                    print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
            
        #handles [Name1] and [Name2] are siblings
        elif "are siblings" in statement:
            sibling1, sibling2 = self._extract_names(statement.replace(" are siblings", ""), " and ")
            try:
                self.prolog.assertz(f"sibling({sibling1.lower()}, {sibling2.lower()})")
                self.prolog.assertz(f"sibling({sibling2.lower()}, {sibling1.lower()})")
                print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        else:
            print("Invalid statement. Please follow the sentence patterns.")


    def process_question(self, question):
        # Handle the "Is [Parent] the father of [Child]" question
        if "Is" in question and "the father of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            parent, child = self._extract_names(modified_question, "the father of")
            result = list(self.prolog.query(f"father({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")
        # Handle the "Is [Person1] the brother of [Person2]" question
        elif "Is" in question and "the brother of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            person1, person2 = self._extract_names(modified_question, "the brother of")
            result = list(self.prolog.query(f"brother({person1.lower()}, {person2.lower()})"))
            print("Yes!" if result else "No!")
        # Handle the "Is [Person1] the sister of [Person2]" question
        elif "Is" in question and "the sister of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            person1, person2 = self._extract_names(modified_question, "the sister of")
            result = list(self.prolog.query(f"sister({person1.lower()}, {person2.lower()})"))
            print("Yes!" if result else "No!")
        # Handle the "Who is the father of [Child]?" question
        elif "Who is the father of" in question:
            child = question.replace("Who is the father of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"father(X, {child.lower()})"))
            if results:
                print(f"The father of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the father of {child} is.")

        # Handle the "Are [Name1] and [Name2] siblings?" question
        elif "Are" in question and "siblings" in question:
            parts = question.replace("Are", "").replace("siblings", "").replace("?", "").split("and")
            if len(parts) == 2:
                person1 = parts[0].strip().lower().capitalize()
                person2 = parts[1].strip().lower().capitalize()
                result = list(self.prolog.query(f"sibling({person1}, {person2})"))
                print("Yes!" if result else "No!")
            else:
                print("Invalid question. Please follow the sentence patterns.")
        # Handle the "Are [Person1] and [Person2] the parents of [Person3]?" question
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

        # Handle the "Is [Parent] the mother of [Child]" question
        elif "Is" in question and "the mother of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            parent, child = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"mother({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")

        # Handle the "Who is the mother of [Child]?" question
        elif "Who is the mother of" in question:
            child = question.replace("Who is the mother of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"mother(X, {child.lower()})"))
            if results:
                print(f"The mother of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the mother of {child} is.")
            # Handle grandparents and grandchildren
        # Handle siblings
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
        # Handle invalid questions
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
        # Handle invalid questions
        elif "Is" in question and "a daughter of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            child, parent = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"daugther({child.lower()}, {parent.lower()})"))
            print("Yes!" if result else "No!")
        # Handle the "Is [Child] the son of [Parent]?" question
        elif "Is" in question and "a son of" in question:
            modified_question = question.replace("Is ", "").replace("?", "").strip()
            child, parent = self._extract_names(modified_question, "the mother of")
            result = list(self.prolog.query(f"son({child.lower()}, {parent.lower()})"))
            print("Yes!" if result else "No!")
        else:
            print("Invalid question. Please follow the sentence patterns.")

    def chat(self):
        print("Welcome to the Family Relationship Chatbot!")
        while True:
            user_input = input("\n> ").strip()
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            elif "?" in user_input:
                self.process_question(user_input)
            else:
                self.process_statement(user_input)

if __name__ == "__main__":
    chatbot = FamilyChatbot("kb.pl")
    chatbot.chat()
