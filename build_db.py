import chromadb

# Initialize local ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="clinical_guidelines")

# 1. Migraine Guideline (Existing)
migraine_guideline = """
CLINICAL GUIDELINE: PRIMARY MIGRAINE MANAGEMENT
Symptoms: Unilateral, throbbing headache, photophobia, nausea. Often exacerbated by screen time, stress, and lack of sleep. Family history is a strong indicator.
Objective Testing: No imaging (CT/MRI) or genetic testing is recommended for standard primary migraines presenting with classic symptoms.
Treatment Plan: 
1. Acute: NSAIDs (Ibuprofen 400mg-800mg), Triptans if NSAIDs fail.
2. Lifestyle: Rest in a dark, quiet room. Screen time reduction, hydration, and sleep regulation.
3. Referral: Only refer to neurology if headaches are refractory to standard acute treatments or if red flag symptoms (seizures, sudden worst headache of life) appear.
"""

# 2. Lower Back Pain Guideline
back_pain_guideline = """
CLINICAL GUIDELINE: ACUTE NON-SPECIFIC LOW BACK PAIN
Symptoms: Aching, stiffness, or muscle spasms in the lower lumbar region. Often triggered by lifting or awkward movements. Pain does not radiate below the knee.
Objective Testing: NO IMAGING (X-ray or MRI) is recommended within the first 6 weeks of symptom onset unless "red flags" are present (e.g., loss of bowel/bladder control, severe neurological deficits).
Treatment Plan: 
1. Acute: NSAIDs (Naproxen or Ibuprofen). Muscle relaxants only if spasms are severe.
2. Lifestyle: DO NOT prescribe strict bed rest. Encourage patients to maintain light mobility and normal activities as tolerated. Apply heat to the affected area.
3. Referral: Physical therapy if symptoms persist beyond 4 weeks.
"""

# 3. NEW: Adult Fever Guideline
fever_guideline = """
CLINICAL GUIDELINE: ACUTE FEVER MANAGEMENT IN ADULTS
Symptoms: Elevated body temperature (≥ 100.4°F or 38°C), chills, sweating, muscle aches, fatigue.
Objective Testing: Routine blood work (CBC) or blood cultures are NOT recommended for a standard viral fever lasting less than 3 days without focal symptoms.
Treatment Plan: 
1. Acute: Antipyretics such as Acetaminophen (Tylenol) 500-1000mg or Ibuprofen 400mg to reduce discomfort. DO NOT prescribe antibiotics for standard viral fevers.
2. Lifestyle: Rest, adequate oral hydration, light clothing. Avoid cold baths or alcohol rubs.
3. Referral: Seek immediate emergency care if fever exceeds 103°F, lasts longer than 3 days, or is accompanied by red flag symptoms.
"""

# Upsert all documents (upsert prevents errors if docs already exist)
collection.upsert(
    documents=[migraine_guideline, back_pain_guideline, fever_guideline],
    metadatas=[{"source": "Neurology_Guidelines_2026"}, {"source": "Ortho_Guidelines_2026"}, {"source": "Internal_Med_Guidelines_2026"}],
    ids=["doc_1", "doc_2", "doc_3"]
)
print("Vector database updated with 3 guidelines using upsert!")
