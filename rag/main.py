import argparse
import pandas as pd
from RAG.chunk_data import sliding_window
from RAG.index_data import store_embedding
from pinecone import Pinecone
from model.embedding_model import Encoder
import os


def main():
    """
    Main function to process, embed, and index Tarot data.

    This script performs several steps:
    1. Parses command-line arguments for various configurations such as model path, sequence length, chunk size, etc.
    2. Reads and chunks Tarot data into smaller text pieces.
    3. Loads a transformer model and encodes these text chunks into embeddings.
    4. Either retrieves an existing Pinecone index or creates a new one and stores the embeddings.

    Command-line Arguments:
    --model_path: Path to the transformer model.
    --max_seq_len: Maximum sequence length for the model.
    --chunk_size: Size of text chunks.
    --step_size: Step size for the sliding window in text chunking.
    --top_k: Number of top contexts to retrieve.
    --index_name: Name for the Pinecone index.
    --API_key: API key for Pinecone services.
    """
    parser = argparse.ArgumentParser(description='aipi590')
    parser.add_argument('--model_path', type=str, default= "BAAI/bge-large-en-v1.5")
    parser.add_argument('--max_seq_len', type=int, default=1024)
    parser.add_argument('--chunk_size', type=int, default=300)
    parser.add_argument('--step_size', type=int, default=200)
    parser.add_argument('--top_k', type=int, default=3)
    parser.add_argument('--index_name', type=str, default="astrology-bot")
    parser.add_argument('--API_key', type=str, default=os.getenv("PINECONE"))
    args = parser.parse_args()
    
    
    print("Starting chunking wiki text data!")
    tarot_data = pd.read_csv('./data/tarot.csv').values.tolist()
    chunks, chunks_topic = sliding_window(tarot_data, args.chunk_size, args.step_size)


    print("Starting chunks embedding!")
    # load LLM as embedding encoder
    model = Encoder(args.model_path, args.max_seq_len)
    # embed chunks 
    chunks_embedding = model.encode(chunks, show_progress_bar=True)
    
    # output A pandas DataFrame containing the precomputed embeddings of the corpus with columns 'embedding' and 'text', store to a parquet file in location: ./data/embeddings.parquet
    print("Storing chunks embedding!")
    embedding_df = pd.DataFrame({"text": chunks, "embedding": chunks_embedding.tolist()})

    # store embedding to parquet file
    embedding_df.to_parquet("./data/embeddings.parquet")

    
    print("Indexing chunks embedding!")
    # create new index if you do not have well-build index
    try:
        pc = Pinecone(api_key=args.API_key)
        index = pc.Index(args.index_name)
    except:
        index = store_embedding(chunks_embedding, chunks, chunks_topic, args.index_name, args.API_key)
    
if __name__ == "__main__":
    main()