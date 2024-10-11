from llm.memory import Memory
from llm.Sawa_State import SawaState 
MEMORY_PROMPT = "\nGiven only the information above, what are 3 most salient high-level questions we can answer about the subjects in the conversation? Separate each question and answer pair with \"{qa}\", and only output the question and answer, no explanations."

class ChatHandler:
    def __init__(self):
        self.memory = Memory()
        self.sawa_state = SawaState()

    def process_chat(self, input_text):
        self.sawa_state.add_message(input_text)
        injections = self.sawa_state.get_injections()
        prompt = self.create_prompt(input_text, injections)
        llm_response = self.call_llm(prompt)
        self.memory.save_to_memory(input_text, llm_response)
        return llm_response

    def create_prompt(self, input_text, injections):
        return f"{injections}\nUser input: {input_text}"

    def call_llm(self, prompt):
        return f"LLM response to: {prompt}"

    def generate_questions_and_answers(self, conversation_data):
        prompt = MEMORY_PROMPT.format(qa="{qa}")
        conversation_text = "\n".join(f"User: {msg['user_name']} said: {msg['user_chat']}" for msg in conversation_data)
        full_prompt = f"{conversation_text}\n{prompt}"
        qa_pairs = self.call_llm(full_prompt)  
        return qa_pairs

    def check_and_reflect(self, messages, global_state):
        if len(messages) >= 10: 
            topic = self.generate_topic_from_messages(messages)
            global_state.set_user_input('youtube_topic', topic)
            qa_pairs = self.generate_questions_and_answers(messages)
            print(f"Generated Q&A Pairs:\n{qa_pairs}")
