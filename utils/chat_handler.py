from llm.memory import Memory  # Assuming you have a Memory class to handle storage
from llm.Sawa_State import SawaState 
MEMORY_PROMPT = "\nGiven only the information above, what are 3 most salient high-level questions we can answer about the subjects in the conversation? Separate each question and answer pair with \"{qa}\", and only output the question and answer, no explanations."

class ChatHandler:
    def __init__(self):
        self.memory = Memory()
        self.sawa_state = SawaState()

    def process_chat(self, input_text):
        """Process the incoming chat input."""
        self.sawa_state.add_message(input_text)
        injections = self.sawa_state.get_injections()
        prompt = self.create_prompt(input_text, injections)
        llm_response = self.call_llm(prompt)
        self.memory.save_to_memory(input_text, llm_response)
        return llm_response

    def create_prompt(self, input_text, injections):
        """Create the LLM prompt with the input text and injections."""
        return f"{injections}\nUser input: {input_text}"  # Example format

    def call_llm(self, prompt):
        """Call the LLM with the current context and input."""
        return f"LLM response to: {prompt}"  # Replace this with actual LLM call logic

    def generate_questions_and_answers(self, conversation_data):
        """Generate high-level questions and answers based on the conversation."""
        prompt = MEMORY_PROMPT.format(qa="{qa}")  # Use the MEMORY_PROMPT
        # Prepare the conversation history or chat data as input
        conversation_text = "\n".join(f"User: {msg['user_name']} said: {msg['user_chat']}" for msg in conversation_data)
        full_prompt = f"{conversation_text}\n{prompt}"

        # Call the LLM or your processing function
        qa_pairs = self.call_llm(full_prompt)  # Assuming `call_llm` handles LLM calls
        return qa_pairs

    def check_and_reflect(self, messages, global_state):
        """Check for reflection after processing a number of messages."""
        if len(messages) >= 10:  # Change threshold to 10
            # Generate a topic based on user messages
            topic = self.generate_topic_from_messages(messages)
            # Send the topic to global_state as a user input
            global_state.set_user_input('youtube_topic', topic)

            # Optionally generate high-level questions and answers
            qa_pairs = self.generate_questions_and_answers(messages)
            print(f"Generated Q&A Pairs:\n{qa_pairs}")
