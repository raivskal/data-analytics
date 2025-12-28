from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)

# pip install llama-index-llms-ollama
# pip install llama-index-readers-file
# pip install llama-index-embeddings-ollama

Settings.llm = Ollama(model="tinyllama", request_timeout=200.0)

# Initialize the Ollama embedding model
embed_model = OllamaEmbedding(model_name="all-minilm")

# Set the embedding model in LlamaIndex settings
Settings.embed_model = embed_model


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query(
    "What are the first programs Paul Graham tried writing?")
print(response)
