import os
import openai
from .resume import my_resume
# from .embedding import query_collection

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# def process_rag_request(query, collection_name, additional_context=None):
#     # Query the vector database for relevant documents
#     retrieval_results = query_collection(collection_name, query)
    
#     # Extract the document content from results
#     documents = []
#     if retrieval_results and 'documents' in retrieval_results:
#         documents = retrieval_results['documents'][0]
    
#     # Construct context from retrieved documents
#     context = "\n\n".join(documents)
    
#     # Add any additional context if provided
#     if additional_context:
#         context = f"{context}\n\nAdditional context: {additional_context}"
    
#     # Construct the prompt for OpenAI
#     prompt = f"""Answer the following question based on the provided context. 
#     If the answer cannot be derived from the context, say "I don't have enough information to answer this question."
    
#     Context:
#     {context}
    
#     Question: {query}
#     """
    
#     # Call OpenAI API
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.5,
#         max_tokens=500
#     )
    
#     return response.choices[0].message.content

def process_simple_request(chat_history: list):
    system_prompt  = f"""
    You are an AI Chatbot for a website portfolio:joelanzi.vercel.app, 
    that can answer questions about Joe's portfolio, projects, blogs, and resume. 
    But right now it's still in the works, which means more details will be added soon.
    So you can answer their questions but always say a short disclaimer. 
    For now, the users can just chat with the AI for now.

    Summarize your answers for now, unless they ask for specifics. DO NOT provide too much detail.

    This is my resume if you need it: {my_resume}
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=500
    )
    
    return response.choices[0].message.content
