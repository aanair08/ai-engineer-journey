import chromadb


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

def store_chunks(chunks, filename):
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{filename}_{i}"],
            metadatas=[{
                "filename": filename
            }]
        )
  

def search(query, filenames=None):
    where_filter = None

    if filenames:
        where_filter = {
            "filename": {"$in": filenames}
        }

    results = collection.query(
        query_texts=[query],
        n_results=3,
        where=where_filter
    )

    return results["documents"][0]