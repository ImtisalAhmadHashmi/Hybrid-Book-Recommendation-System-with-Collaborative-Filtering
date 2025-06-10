import numpy as np
import pandas as pd
import streamlit as st
from fuzzywuzzy import process

#Function for the most popular books
def top_50_popular_books(df_books, df_ratings):
  #merging books and rating dataframe
  df_books_ratings = df_books.merge(df_ratings, on='ISBN')

  #geting total number of rating for each book
  df_books_rating_count = df_books_ratings.groupby('Book-Title')['Book-Rating'].count().reset_index()
  df_books_rating_count.rename(columns={'Book-Rating':'num_ratings'},inplace=True)

  #geting mean of all ratings for each book
  df_books_rating_avg = df_books_ratings.groupby('Book-Title')['Book-Rating'].mean().reset_index()
  df_books_rating_avg.rename(columns={'Book-Rating':'avg_ratings'},inplace=True)

  #merging newly created dataframes with average and count
  good_books = df_books_rating_count.merge(df_books_rating_avg,on='Book-Title')

  #merging these new columns with the main dataframe and picking only the useful columns
  good_books = good_books.merge(df_books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Year-Of-Publication','Publisher','Image-URL-M','num_ratings','avg_ratings']]

  #taking log of the rating count column
  good_books["num_ratings"] = np.log(good_books["num_ratings"] + 1)

  #creating a column to give weightage to the age of the book
  good_books["Year-Of-Publication"] = pd.to_numeric(good_books["Year-Of-Publication"], errors='coerce')
  good_books["year_weight"] = good_books["Year-Of-Publication"].apply(lambda x: 1 + (2025 - x) *0.02)

  #creating a column with calculated popularity score
  good_books["popularity_score"] = good_books["num_ratings"] * good_books["avg_ratings"] * good_books["year_weight"]

  #final dataframe with top 50 most popular books
  good_books = good_books[good_books['num_ratings']>=np.log(350 +1)].sort_values("popularity_score", ascending = False).head(50)

  return good_books


def display_popular(dataset):
  cols = st.columns(4)

  for loc in range(50):
    book_title = dataset["Book-Title"].iloc[loc]
    author = dataset["Book-Author"].iloc[loc]
    year = dataset["Year-Of-Publication"].iloc[loc]
    publisher = dataset["Publisher"].iloc[loc]
    pic = dataset["Image-URL-M"].iloc[loc]
    col = cols[loc % 4]
    with col:
      st.image(pic, use_container_width=True)
      st.write(f"""
      **Book Title:**      {book_title}\n\n
      **Author :**         {author}\n\n
      **Publishing Year:** {int(year)}\n\n
      **Publisher:**       {publisher}""")


# Functions for the books recommendations
def pivot_table(df_books, df_ratings):

  df_books_ratings = df_books.merge(df_ratings, on='ISBN')

  x = df_books_ratings.groupby("User-ID")["Book-Rating"].count() > 200
  high_frq_rating_users =x[x].index
  filtered_dataset = df_books_ratings[df_books_ratings["User-ID"].isin(high_frq_rating_users)]

  y = filtered_dataset.groupby("Book-Title")["Book-Rating"].count() >= 50
  high_frq_rated_books = y[y].index
  filtered_dataset = filtered_dataset[filtered_dataset["Book-Title"].isin(high_frq_rated_books)]

  df_user_book_rating = filtered_dataset.pivot_table(index="Book-Title", columns = "User-ID", values = "Book-Rating")

  df_user_book_rating.fillna(0,inplace=True)

  return df_user_book_rating, filtered_dataset


def get_book_suggestions(book_name, df):
  matches = process.extract(book_name, df.index, limit=10)
  suggestions = []
  for i, (match, score) in enumerate(matches, 1):
    suggestions.append(match)
  return suggestions

def recommendation(book_name,lowercase_title, similarity_score ):
  book_name = str(book_name.lower())

  index = lowercase_title.index(book_name)

  # Get similar books
  similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]

  return similar_books, index

def show_recommendations(recommendations,df_pv,book_name, df_fl, index ):
  cols = st.columns(4)
  loc = 0
  st.write(f"\nRecommendations for {df_pv.index[index]}:")
  for i, (idx, score) in enumerate(recommendations, 1):
    book_recommended = df_pv.index[idx]
    row = df_fl.loc[df_fl["Book-Title"] == book_recommended]
    book_author = row["Book-Author"].iloc[0]
    year_of_publication = row["Year-Of-Publication"].iloc[0]
    publisher = row["Publisher"].iloc[0]
    pic = row["Image-URL-M"].iloc[0]

    col = cols[loc % 4]
    loc += 1
    with col:
      st.image(pic, use_container_width=True)
      st.write(f"""
       {i}. {book_recommended}\n\n
       **Author:**                 {book_author}\n\n
       **Year Of Publication:**    {year_of_publication}\n\n
       **Publisher:**              {publisher}\n\n
       similarity score with {book_name} :- ({score:.2f})""")
