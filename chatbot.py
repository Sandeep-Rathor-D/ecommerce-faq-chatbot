from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAQ data
df = pd.read_csv('faq_data.csv')
questions = df['question'].tolist()
answers = df['answer'].tolist()

# Convert FAQ questions to embeddings
faq_embeddings = model.encode(questions, convert_to_tensor=True)

def get_answer(user_query):
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(query_embedding, faq_embeddings)[0]

    top_scores, top_indices = similarity_scores.topk(3)

    # If highest score is good enough
    if top_scores[0] > 0.6:
        return answers[top_indices[0].item()]
    else:
        suggestions = [f"• {questions[i]} — {answers[i]}" for i in top_indices]
        return (
            "Sorry, I couldn't find an exact match. But here are some similar questions:\n\n"
            + "\n\n".join(suggestions)
        )
