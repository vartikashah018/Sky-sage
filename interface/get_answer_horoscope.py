from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
import os

class LlaMA2_Horoscope:
    """
    A class for generating results given questions using a LLaMA-2 model.
    """
    def __init__(self, checkpoint, max_seq_len = 512, device='cuda:0',API_KEY=None):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.tokenizer = LlamaTokenizer.from_pretrained(checkpoint)
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        if API_KEY is not None:
            self.model = LlamaForCausalLM.from_pretrained(checkpoint,torch_dtype=torch.float16, token = API_KEY).to(self.device)  
        else:
            self.model = LlamaForCausalLM.from_pretrained(checkpoint,torch_dtype=torch.float16).to(self.device)
        self.max_seq_len = max_seq_len

    def predict(self, text):
        inputs = self.tokenizer.encode(text, return_tensors='pt', max_length=self.max_seq_len, truncation=True)
        inputs = inputs.to(self.device)
        
        # Calculate the maximum length for the model generation
        output_max_length = len(inputs[0]) + self.max_seq_len
        
        outputs = self.model.generate(inputs, max_length=output_max_length)
        full_output =  self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return full_output

def get_answer_horoscope(
    inference_model_path = "chloeliu/llama-2-7b-chat-horoscope",
    question = None,
    ):

    """
    Retrieves an answer for a given question or computes the QA accuracy on a test dataset using LLaMA-2-7B model.

    :param embedding_model_path: Path to the embedding model.
    :param inference_model_path: Path to the LLaMA-2-7B inference model.
    :param top_k: The number of top contexts to retrieve for the question.
    :param question: The question to be answered. If None, the function computes QA accuracy on a test dataset.

    :return: If a question is provided, returns a tuple (answer, context). 
             If no question is provided, ask for a question.
    """

    
    # get embedding model and LLaMA-2-&B model
    inference_model = LlaMA2_Horoscope(inference_model_path, max_seq_len = 256)
    answer = inference_model.predict(question)
    
    return answer