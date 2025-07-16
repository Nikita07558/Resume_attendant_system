import json
import numpy as np
from sentence_transformers import SentenceTransformer


with open("utils/onet_skills.json", "r") as f:
    skills = json.load(f)


model = SentenceTransformer("all-MiniLM-L6-v2")
skill_vectors = model.encode(skills, show_progress_bar=True)

np.save("utils/skills_matrix.npy", skill_vectors)
print("✅ Saved utils/skills_matrix.npy")
