import os
import json
from flask import Flask, request, jsonify
import openai
import pinecone

app = Flask(__name__)

# Load API keys from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_environment = os.environ.get("PINECONE_ENVIRONMENT")

# Initialize Pinecone connection (replace with your index name)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = "your-index-name"  # Replace with your actual index name
index = pinecone.Index(index_name)

@app.route('/query', methods=['POST'])
def query_endpoint():
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({"error": "Missing 'question' in the request body"}), 400
        
        # Generate embedding (replace with your preferred embedding model)
        embedding_response = openai.Embedding.create(
            input=question,
            model="text-embedding-ada-002" 
        )
        question_embedding = embedding_response['data'][0]['embedding']

        # Query Pinecone index
        query_results = index.query(
            vector=question_embedding,
            top_k=3,  # Adjust as needed
            include_metadata=True
        )
        
        context = ""
        for result in query_results['matches']:
            context += result['metadata']['text'] + " "

        # Use LLM to generate an answer (replace with your preferred LLM)
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        llm_response = openai.Completion.create(
            engine="text-davinci-003",  # or other suitable model
            prompt=prompt,
            max_tokens=150  # Adjust as needed
        )
        answer = llm_response['choices'][0]['text'].strip()
        
        return jsonify({"answer": answer})

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {e}"}), 500
    except pinecone.core.exceptions.PineconeException as e:
        return jsonify({"error": f"Pinecone error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)