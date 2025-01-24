import pandas as pd
from tqdm import tqdm


def sliding_window(tarrot_data, chunck_size = 20, step_size=10):
    
    """
    Dividing text into chunks using a sliding window approach.

    :param chunck_size: The number of words in each text chunk (default is 20).
    :param step_size: The step size for the sliding window to move over the text (default is 10).

    :return: A tuple of two lists: 
             - The first list contains chunks of text.
             - The second list contains the corresponding topics for each chunk.
    """
    chunks = []
    chunks_topic =  []
    sub_topics = ['upright_keywords','reverse_keywords','description','upright','reversed']

    for i in tqdm(range(len(tarrot_data))):
        card = tarrot_data[i][1]
        upright_keywords = tarrot_data[i][2]
        reverse_keywords = tarrot_data[i][3]
        description = tarrot_data[i][4]
        upright = tarrot_data[i][5]
        reversed = tarrot_data[i][6]

        topic_upright = card + '_upright'
        text_upright = upright_keywords + ' ' + description + ' ' + upright
        words_upright = text_upright.split()
    
        for i in range(0, len(words_upright) - chunck_size + 1, step_size):
            chunks.append(" ".join(words_upright[i:i + chunck_size]))
            chunks_topic.append(topic_upright)
        
        topic_reversed = card + '_reversed'
        text_reversed = reverse_keywords + ' ' + description + ' ' + reversed
        words_reversed = text_reversed.split()
    
        for i in range(0, len(words_reversed) - chunck_size + 1, step_size):
            chunks.append(" ".join(words_reversed[i:i + chunck_size]))
            chunks_topic.append(topic_reversed)

    return chunks, chunks_topic