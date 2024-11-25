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
        if "is the father of" in statement:
            parent, child = self._extract_names(statement, "is the father of")
            try:
                self.prolog.assertz(f"male({parent.lower()})")
                self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        elif "is the mother of" in statement:
            parent, child = self._extract_names(statement, "is the mother of")
            try:
                self.prolog.assertz(f"female({parent.lower()})")
                self.prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                print("OK! I learned something.")
            except Exception as e:
                print(f"That’s impossible! {e}")
        else:
            print("Invalid statement. Please follow the sentence patterns.")


    def process_question(self, question):
        # Handling the father-child relationship
        if "Is" in question and "the father of" in question:
            parent, child = self._extract_names(question, "is the father of")
            result = list(self.prolog.query(f"father({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")

        # Handling the "Who is the father of" question
        elif "Who is the father of" in question:
            child = question.replace("Who is the father of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"father(X, {child.lower()})"))
            if results:
                print(f"The father of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the father of {child} is.")

        # Handling sibling relationship query
        elif "Are" in question and "siblings" in question:
            person1, person2 = self._extract_names(question, "are siblings")
            result = list(self.prolog.query(f"sibling({person1.lower()}, {person2.lower()})"))
            print("Yes!" if result else "No!")

        # Handling the "Is X the mother of Y?" question
        elif "Is" in question and "the mother of" in question:
            parent, child = self._extract_names(question, "is the mother of")
            result = list(self.prolog.query(f"mother({parent.lower()}, {child.lower()})"))
            print("Yes!" if result else "No!")

        # Handling the "Who is the mother of X?" question
        elif "Who is the mother of" in question:
            child = question.replace("Who is the mother of", "").strip().replace("?", "")
            results = list(self.prolog.query(f"mother(X, {child.lower()})"))
            if results:
                print(f"The mother of {child} is {results[0]['X'].capitalize()}.")
            else:
                print(f"I don’t know who the mother of {child} is.")

        # If none of the valid patterns are found
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
