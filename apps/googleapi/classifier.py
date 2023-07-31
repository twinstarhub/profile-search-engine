from sentence_transformers import SentenceTransformer, util
import itertools

# Function to calculate cosine similarity between sentence embeddings
def calculate_similarity(embeddings):
    avg_sim = util.pytorch_cos_sim(embeddings, embeddings).mean().item()
    return avg_sim

# String lists representing profiles in different groups (platforms)
platform1_profiles = [
    "Michael Bage is a software engineer who loves coding.",
    "michael123 is my username for this platform.",
    "Contact me at john@example.com for more information.",
    "Location: New York",
    "Interests: Photography, Travel",
    "Education: Bachelor's in Computer Science",
    "Job: Software Engineer",
    "About: I love coding and building applications."
]

platform2_profiles = [
    "Alice Smith is passionate about art and design.",
    "alicesmith is my username for this platform.",
    "You can reach me at alice.smith@mail.com.",
    "Location: Los Angeles",
    "Interests: Travel, Cooking",
    "Education: Master's in Business Administration",
    "Job: Marketing Manager",
    "About: Passionate about art and design."
]

platform3_profiles = [
    "Michael Johnson is interested in data science.",
    "michael_j is my username for this platform.",
    "Email: michael.johnson@gmail.com",
    "Location: London",
    "Interests: Photography, Gardening",
    "Education: Engineering Degree",
    "Job: Data Scientist",
    "About: Traveling the world and capturing moments."
]

platform4_profiles = [
    "Akira Taro enjoys hiking and exploring nature.",
    "emily_brown is my username for this platform.",
    "Contact me at emily.b@example.com",
    "Location: Sydney",
    "Interests: Gardening",
    "Education: Art History",
    "Job: Graphic Designer",
    "About: Exploring the wonders of nature."
]

# Combine all profiles to form the profile information set for each platform
platform_profiles = [platform1_profiles, platform2_profiles, platform3_profiles, platform4_profiles]

# Initialize the Sentence Transformers model
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Encode the profiles into embeddings for all platforms
all_embeddings = [model.encode(profiles, convert_to_tensor=True) for profiles in platform_profiles]

# Calculate the similarity between all combinations of one profile from each platform
max_sim = 0.0
max_profiles = None

for profiles in itertools.product(*platform_profiles):
    embeddings = [model.encode(profile, convert_to_tensor=True) for profile in profiles]
    avg_sim = calculate_similarity(embeddings)
    if avg_sim > max_sim:
        max_sim = avg_sim
        max_profiles = profiles

# Print the most similar profiles from each platform
if max_profiles is not None:
    print(f"Highest Similarity: {max_sim:.4f}")
    print("\n".join(max_profiles))
