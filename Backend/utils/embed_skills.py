import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load raw skills list
with open("utils/onet_skills.json", "r") as f:
    skills = json.load(f)

# Embed all skills
model = SentenceTransformer("all-MiniLM-L6-v2")
skill_vectors = model.encode(skills, show_progress_bar=True)

# Save to disk
np.save("utils/skills_matrix.npy", skill_vectors)
print("✅ Saved utils/skills_matrix.npy")
