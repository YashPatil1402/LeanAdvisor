from database import problems
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load pre-trained model
print("Loading AI model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully.\n")


# Store all problems
problem_database = []


# Flatten database
for category_name, category in problems.items():

    for problem_name, details in category.items():

        search_text = (

            problem_name + " " +

            details["waste"] + " " +

            details["principle"] + " " +

            details["principle_explanation"] + " " +

            " ".join(details["tools"]) + " " +

            " ".join(details["root_causes"]) + " " +

            " ".join(details["benefits"]) + " " +

            " ".join(details["preventive_measures"]) + " " +

            " ".join(details["corrective_measures"])

        )

        problem_database.append({

            "category": category_name,

            "problem": problem_name,

            "details": details,

            "text": search_text

        })


# Create embeddings for all problems
print("Generating embeddings for database...")

problem_texts = [

    item["text"]

    for item in problem_database

]

problem_embeddings = model.encode(

    problem_texts,

    convert_to_tensor=False

)

print("Database embeddings created.\n")


def search_problem(user_input, top_n=3):

    # Convert query into embedding
    query_embedding = model.encode(

        [user_input],

        convert_to_tensor=False

    )

    # Compute similarity
    similarity_scores = cosine_similarity(

        query_embedding,

        problem_embeddings

    )[0]

    # Top results
    top_indices = similarity_scores.argsort()[::-1][:top_n]

    results = []

    for idx in top_indices:

        results.append({

            "similarity":

            round(similarity_scores[idx] * 100, 2),

            "category":

            problem_database[idx]["category"],

            "problem":

            problem_database[idx]["problem"],

            "details":

            problem_database[idx]["details"]

        })

    return results


# Test mode
if __name__ == "__main__":

    while True:

        query = input("\nEnter problem (or 'exit'): ")

        if query.lower() == "exit":

            break

        matches = search_problem(query)

        print("\nTop Matches\n")

        for i, match in enumerate(matches, start=1):

            details = match["details"]

            print("=" * 80)

            print(f"Match {i}")

            print(f"Similarity : {match['similarity']} %")

            print(f"Category   : {match['category']}")

            print(f"Problem    : {match['problem']}")

            print(f"Waste      : {details['waste']}")

            print(f"Principle  : {details['principle']}")

            print("\nTools:")

            for tool in details["tools"]:

                print("-", tool)

            print("\nRoot Causes:")

            for cause in details["root_causes"]:

                print("-", cause)

            print("\nBenefits:")

            for benefit in details["benefits"]:

                print("-", benefit)

            print("\nPreventive Measures:")

            for measure in details["preventive_measures"]:

                print("-", measure)

            print("\nCorrective Measures:")

            for measure in details["corrective_measures"]:

                print("-", measure)

            print()