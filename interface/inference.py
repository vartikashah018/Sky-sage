import argparse
import pandas as pd
from model.embedding_model import Encoder
from model.inference_model import LlaMA2
from interface.get_response import retrieve_context, ask_question
import numpy as np
from tqdm import tqdm
import os
import sys
import torch
import random
sys.path.insert(1, os.getcwd())

def seed_everything(seed: int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    
seed_everything(32)


def get_answer(
    embedding_model_path = "BAAI/bge-large-en-v1.5",
    inference_model_path = "meta-llama/Llama-2-7b-chat-hf",
    top_k = 2,
    question = None,
    cards = None,
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
    embedding_model = Encoder(embedding_model_path, 512)
    inference_model = LlaMA2(inference_model_path, API_KEY=os.environ.get("HF_TOKEN"), max_seq_len=1024)
    
    # load embeddings
    embedding_df = pd.read_parquet("./data/embeddings.parquet")
    
    # few_shots_df = {0: {'prompt': '''
    #                     Chloe is 23 years old and single, having recently been ‘ghosted’ by someone she’d been seeing.

    #                     She is learning tarot on her own, and knows to focus her question on her own power to find love. She says she’s tempted to ask, “Why did he ditch me? Does he still have feelings for me?” But she knows that those answers won’t help her in the long run, and will just serve to relinquish her energy to someone who does not deserve it. After meditating on her feelings, she decides to word the question this way:

    #                     “What is something I should know about my love life, and how can I move forward in the best way?”
    #                     ''',

    #                     'cards': '''
    #                     The Queen of Summer (Cups) and the Herald of Spring (Page of Wands), cards 1 and 3, show upside-down. 
    #                     The Fool is a crossing card, and is non-directional. 
    #                     The Hermit shows rightside-up in the crown position.
    #                     ''',

    #                     'answer': 

    #                     '''Chloe, according to these cards, you carry within you the potential for emotional wisdom (Queen of Cups), but also the risk of impulsive behavior (Fool). These cards lovingly ask you to be very picky in your love life and to not rush things. Your romantic behavior should be one part action to three parts reflection. Learning about love is a biggie for you in this lifetime, and even small experiences will affect you profoundly.
    #                     For the time being, this reading says to be patient about love (Hermit). Don't let others tell you what to do or believe. Don’t get caught in small passions with lesser people (Page of Wands, reversed). You are the Queen of Cups-in-training. Let yourself mature into this role by falling deeply in love with yourself first.
    #                     '''
                        
    #                     },

    #                 1: {'prompt': '''
    #                     Lois, is in the market for a house.

    #                     After a long search, she has found a property she is interested in. It checks a lot of boxes on her wishlist: two acres of land, a large house and with a couple of smaller structures – all within her budget. It’s a fixer-upper (as she had wanted), and though she is slightly daunted by the amount of work it needs, she has learned from an inspection that the home is structurally sound. She asks you, 
                        
    #                     “Is this the house of my dreams or my nightmares?”''',
                            
    #                     'cards': '''
    #                     CARD 1 (An energetic representation of the property): Knight of Wands
    #                     CARD 2 (Its strong points for Lois): The Sun 
    #                     CARD 3 (Its troubles for Lois): Seven of Swords
    #                     CARD 4 (The potential for Lois to be pleased with this place): Five of Cups, reversed
    #                     ''',

    #                     'answer': 
    #                     '''
    #                     Lois, these cards reflect your excitement and optimism for the place, but there is a twist in the message that is discouraging.

    #                     Overall, the property and the transaction hold high energy for you. The Knight of Wands shows you making a bold and strong move in a new direction with this property. You may feel that there is competition and you need to move quickly to get it. This Knight is assertive, but can also be impulsive.


    #                     With the positive side showing as the Sun, you are given a vote of confidence. This card is all about joy and feeling like you are where you should be. You describe this as possibly the home of your dreams. It very well may be, according to this card.


    #                     However, there is a downside showing in the next 2 cards. The Seven of Swords is a warning to keep a skeptical eye on the details. It says that there has been some dishonesty in the past. Please be careful of any potential misrepresentations in the paperwork. (If you are an astrologer, you know that Mercury is retrograde right now. Check all documents carefully).


    #                     I have two possible interpretations for your final card, the Five of Cups. In general, this card is about sadness and learning to appreciate the bright side of things. Upside down, it is about emotional healing, letting go of sadness, moving on. If you end up here, it looks like it would likely be a very healing place for you. As a direct answer to your question — “is this my dream or my nightmare?” — this card seems to say that it's a place where you can wake up from a sad dream and find yourself in the warmth of the Sun. This is my primary feeling from this card.

    #                     Another possibility, however, is that the Five of Cups shows potential disappointment at the loss of a sale. If you decide you want this place, these cards encourage you to move carefully but swiftly, be alert for any signs of dishonesty, and really put your will to work.

    #                     '''
                        
    #                     }
    #                     }


    # # merge few_shot samples into prompt
    # few_shots = []
    # for i in range(2):
    #     prompt = few_shots_df[i]['prompt']
    #     cards_shot = few_shots_df[i]['cards']
    #     answer = few_shots_df[i]['answer']
    #     question_shot = f"""
    #         Question: {prompt}\n
    #         Cards: {cards_shot}\n
    #         ### Response: {answer}\n
    #         """
    #     few_shots.append(question_shot)

    # few_shots = " \n ".join(few_shots)


    
    context = retrieve_context(question, cards, embedding_df, embedding_model, top_k)
    # answer = ask_question(question, few_shots, context, inference_model, cards)
    answer = ask_question(question, context, inference_model, cards)
    
    return answer, context