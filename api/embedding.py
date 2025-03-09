# import chromadb
# import os
# from chromadb.config import Settings
# from chromadb.utils import embedding_functions

# # Configure ChromaDB client
# # For serverless, we'll use an in-memory instance or persistent directory
# def get_chroma_client():
#     # Using an in-memory client for serverless functions
#     client = chromadb.Client(Settings(
#         chroma_db_impl="duckdb+parquet",
#         persist_directory=".chromadb" # This path needs to be in /tmp for Vercel
#     ))
#     return client

# # Initialize OpenAI embeddings function
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=os.environ.get("OPENAI_API_KEY"),
#     model_name="text-embedding-3-small"
# )

# def get_or_create_collection(collection_name):
#     client = get_chroma_client()
#     collection = client.get_or_create_collection(
#         name=collection_name,
#         embedding_function=openai_ef
#     )
#     return collection

# def query_collection(collection_name, query_text, n_results=3):
#     collection = get_or_create_collection(collection_name)
#     results = collection.query(
#         query_texts=[query_text],
#         n_results=n_results
#     )
#     return results
