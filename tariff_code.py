'''
Question 2: Tariff Code Classifier (String Matching + Trie)
Problem:
Build a system to classify products into Harmonized System (HS) tariff codes based on keywords.
HS codes are hierarchical (e.g., 8471 = machines, 8471.30 = portable computers).
python# HS Code database
hs_codes = {
    "8471": ["computer", "processor", "laptop", "desktop"],
    "8471.30": ["laptop", "notebook", "portable computer"],
    "8471.41": ["desktop", "tower", "workstation"],
    "8517": ["phone", "telephone", "smartphone"],
    "8517.12": ["smartphone", "mobile phone", "cellular"]
}

# Test cases
products = [
    "Apple MacBook Pro Laptop 16-inch",  # Should match 8471.30
    "iPhone 15 Pro Smartphone",           # Should match 8517.12
    "Dell Desktop Computer Tower",        # Should match 8471.41
    "Gaming Laptop with RTX GPU"         # Should match 8471.30
]
Requirements:

Match products to most specific HS code possible
Handle partial matches and synonyms
Return confidence score (0-1) based on keyword matches
Prioritize longer/more specific code matches

Follow-ups:

How do you handle products with multiple possible classifications?
What if you need to support fuzzy matching for typos?
How would you update the system as new HS codes are added?
Scale to 10M products - what data structure optimizes lookup?

Concepts tested: Trie, string matching, ranking algorithms, prefix search
'''