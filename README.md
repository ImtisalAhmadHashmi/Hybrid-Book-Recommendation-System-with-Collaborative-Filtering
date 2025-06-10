# Hybrid-Book-Recommendation-System-with-Collaborative-Filtering
📚 Bridging Popularity Scores & User Behavior for Personalized Reads\
🔹 Project Flow & Key Technical Steps\
📂 Data Loading & Preprocessing\
•	Datasets Used:\
o	Books.csv (271K entries: ISBN, title, author, publisher, image URLs).\
o	Ratings.csv (1.1M entries: User-ID, ISBN, ratings).\
o	Users.csv (278K entries: User-ID, location, age).\
•	Handled Missing Values:\
o	Dropped nulls in Book-Author/Publisher (Books.csv) and ignored Age (Users.csv) due to 110K+ nulls.\
o	Retained critical columns (ISBN, Book-Rating) with zero nulls for core functionality.\
⚙️ Feature Engineering & Hybrid Approach
1.	Popularity-Based Filtering:\
o	Merged books and ratings data, calculated log-normalized rating counts and weighted average ratings.\
o	Year-Weighted Score: Boosted recent books with 1 + 0.02 × (2025 - Year-Of-Publication).\
o	Final Formula: Popularity Score = log(num_ratings + 1) × avg_rating × year_weight.\
o	Output: Ranked top 50 books (threshold: ≥350 ratings).
2.	Collaborative Filtering:\
o	Pivot Table: Created user-book matrix (rows=books, columns=users) for cosine similarity.\
o	Filtered Data: Kept only high-frequency users (>200 ratings) and frequently rated books (>50 ratings) to reduce sparsity.\
o	Fuzzy Matching: Used fuzzywuzzy to handle typos/mismatches in user search queries.\
🤖 Model & Deployment\
•	Algorithm: Cosine Similarity to find nearest-neighbor books based on user ratings.\
•	Streamlit UI:\
o	Interactive Search: Auto-suggestions for book names with dropdown fallback.\
o	Grid Display: 4-column responsive layout for book covers, titles, authors, and similarity scores.\
o	Dual Output: Shows both personalized recommendations and popular books in one dashboard.\
🚀 Key Achievements\
•	Scalable Preprocessing: Handled 1.1M+ ratings with optimized merging/log-transforms.\
•	Hybrid Logic: Combined content-based (popularity) and collaborative filtering for diverse recommendations.\
•	User-Centric Design: Fuzzy search + visual book displays improved usability.
