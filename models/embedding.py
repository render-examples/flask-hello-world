import openai

def get_embedding(text, model="text-embedding-ada-002"):

  # Get the embedding from the text embedding model.
  embedding = openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

  # Return the embedding.
  return embedding