import os
import pinecone
import openai
import argparse

def connect_to_pinecone(api_key, environment, index_name):
    """Connects to Pinecone."""
    try:
        pinecone.init(api_key=api_key, environment=environment)
        index = pinecone.Index(index_name)
        print(f"Successfully connected to Pinecone index '{index_name}'.")
        return index
    except Exception as e:
        print(f"Error connecting to Pinecone: {e}")
        return None

def upsert_vectors(index, vectors):
    """Upserts vectors to Pinecone."""
    try:
        index.upsert(vectors=vectors)
        print("Vectors upserted successfully.")
    except Exception as e:
        print(f"Error upserting vectors: {e}")

def query_pinecone(index, query_vector, top_k=10):
    """Queries Pinecone."""
    try:
        query_response = index.query(vector=query_vector, top_k=top_k)
        print("Query successful.")
        return query_response
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return None

def generate_embeddings(text):
    """Generates embeddings using OpenAI."""
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.Embedding.create(
            input=text, model="text-embedding-ada-002"
        )
        embeddings = response["data"][0]["embedding"]
        print("Embeddings generated successfully.")
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with Pinecone.")
    parser.add_argument("--api_key", required=True, help="Pinecone API key")
    parser.add_argument("--environment", required=True, help="Pinecone environment")
    parser.add_argument("--index_name", required=True, help="Pinecone index name")
    args = parser.parse_args()

    index = connect_to_pinecone(args.api_key, args.environment, args.index_name)
    
    if index:
        # Example usage (you can remove or modify these lines)
        # example_text = "This is an example text"
        # embeddings = generate_embeddings(example_text)
        # if embeddings:
        #     upsert_vectors(index, [("id1", embeddings)])
        #     query_response = query_pinecone(index, embeddings)
        #     print(query_response)
        pass