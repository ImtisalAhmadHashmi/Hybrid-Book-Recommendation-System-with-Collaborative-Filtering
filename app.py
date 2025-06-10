import pandas as pd
from helper import top_50_popular_books, pivot_table, get_book_suggestions, recommendation, show_recommendations, display_popular
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

#loading the dataset
df_books = pd.read_csv("Books.csv")
df_ratings = pd.read_csv("Ratings.csv")
df_users = pd.read_csv("Users.csv")

st.title("📚 Book Recommendation System")

st.subheader("Book Recommendations through Collaborative Filtering")

#prepareing the dataset
df_user_book_rating, filtered_dataset = pivot_table(df_books, df_ratings)
similarity_score = cosine_similarity(df_user_book_rating)
lowercase_book_titles = [book_title.lower() for book_title in list(df_user_book_rating.index)]

# Create a container for the search box and dropdown
search_container = st.container()

# Get user input
user_input = search_container.text_input(
  "Enter a book name if you want recommendation for the related books:",
  placeholder="Start typing...",
  key="book_search"
)

# Generate and display suggestions dynamically
if user_input.lower not in lowercase_book_titles:
  suggestions = get_book_suggestions(user_input, df_user_book_rating)

  if suggestions:
  # Display the dropdown with suggestions below the search box
    selected_book = search_container.selectbox(
      """Do you mean anyone one of the book in the dropdown option. 
      Can't find your book? (Pardon us we have data of almost 800 books)
      Try another search.""",
      options=suggestions,
      key="book_select_dynamic"
    )

else:
  selected_book = user_input

similar_books, index = recommendation(selected_book, lowercase_book_titles, similarity_score)

if st.button("Generate Recommendations"):
  show_recommendations(similar_books,df_user_book_rating, selected_book, filtered_dataset, index )

st.subheader("Top 50 Most Popular Books through Popularity Score\n"
             "Formula: (log(num_ratings + 1)) × (avg_ratings) × (1 + 0.02 × (Current Year - Year-Of-Publication)))")

good_books = top_50_popular_books(df_books, df_ratings)

display_popular(good_books)