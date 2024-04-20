import google.generativeai as genai

class GenAIExeption (Exception):
         """GenAI Exeption base class """ 
class ChatBot : 
   """Chat can only have one condidate count"""
   CHATBOT_NAME ='My Gemini AI'  
      #initialiser chatbot obj ,
      # Stores the provided API key for authentication with Gemini AI
      #Calls preload_conversation to set up initial conversation history.
   def  __init__(self,api_key ) :
      self.genai = genai
      self.genai.configure(api_key=api_key)
      self.model=self.genai.GenerativeModel('gemini-1.0-pro-latest')
      self.conversation=None
      self._conversation_history = []

      self.preload_conversation()

   def send_prompt(self, prompt,temperature=0.1):
      if temperature < 0 or temperature > 1:
         raise GenAIExeption ('Temperature must be between 0 and 1')    
      if not prompt:
         raise GenAIExeption('prompt cannot be empty')
             
      try: 
         response = self.conversation.send_message(
            content=prompt, 
            generation_config=self._generation_config(temperature),
         )
         response.resolve()
         return f'{response.text}\n' + '---' * 20  
      except Exception as e:
         raise GenAIExeption(e.message)
      
   @property    
   def history(self):#Returns a list of messages in the conversation history
      conversation_history=[
         {'role':message.role, 'text':message.parts[0].text} for message in self.conversation.history
      ]
      return conversation_history
       
   def clear_conversation(self):
      self.conversation =self.model.start_chat(history=[])
   
   def _generation_config(self, temperature):
      #Creates a GenerationConfig object for the Gemini AI model, specifying the desired temperature (randomness).
      return genai.typesGenerationConfig(
      temperature=temperature
      )
       
   def _construct_message(self, text, role='user'):
      return {
         'role':role,
         'parts':[text]
      }
#sois hadi
   def preload_conversation(self, conversation_history=None ):
      if isinstance(conversation_history,list):
         self._conversation_history() # There is no _conversation_history() in ur class
      else:
         self._conversation_history=[
             self._construct_message('From now on ,return the output as a JSON object that can be loaded in python file whith the key as \'text\'.For example,{"text":"<output goes here> "}'),
             self._construct_message('{"text":"sure, I can return the output as a JSON objectwith the key as `text`.Here is an example :{"text":"your Output" }.','model')
          ]
         
   def ChatWithModel(self,message):
      response = self.model.generate_content(message)
      print(response.text)
      return response.text

       