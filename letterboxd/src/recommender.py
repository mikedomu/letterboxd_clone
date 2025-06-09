"""
Module implementing movie recommendation system.
"""


import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    """
    Class implementing feature-based movie recommendation system.

    :param database: Database class instance with database connection.
    :type database: Database
    """

    def __init__(self, database):
        self.database = database
        self.movies = self.database.get_all_movies_as_dataframe()
        self.prepare_features()

    def prepare_features(self):
        """
        Prepares movie features for similarity analysis.
        Processes textual and numerical movie features into vector format.
        """

        self.feature_data = {}

        def vectorize_column(column, tokenizer=None):
            vectorizer = CountVectorizer(tokenizer=tokenizer)
            vector = vectorizer.fit_transform(self.movies[column]).toarray()
            return vector

        self.feature_data['genres'] = vectorize_column('genres', tokenizer=lambda x: x.split(', '))
        self.feature_data['keywords'] = vectorize_column('keywords', tokenizer=lambda x: x.split(', '))
        self.feature_data['cast'] = vectorize_column('cast', tokenizer=lambda x: x.split(', '))
        self.feature_data['director'] = vectorize_column('director', tokenizer=lambda x: x.split(', '))

        self.feature_data['overview'] = vectorize_column('overview')

        # Runtime normalizujemy do zakresu 0-1
        scalar = MinMaxScaler()
        self.feature_data['runtime'] = scalar.fit_transform(self.movies[['runtime']])

    def build_matrix(self, selected_features):
        """
        Builds feature matrix based on selected properties.

        :param selected_features: List of feature names to include in analysis.
        :type selected_features: list[str]
        :return: Feature matrix as numpy array.
        :rtype: numpy.ndarray
        """
        feature_matrices = [self.feature_data[feat] for feat in selected_features]
        return np.hstack(feature_matrices)

    def recommend(self, movie_title, selected_features=None, top_n=10):
        """
        Generates movie recommendations based on similarity to selected movie.

        :param movie_title: Title of the movie to find recommendations for.
        :type movie_title: str
        :param selected_features: List of features used for similarity calculation.
        :type selected_features: list[str] or None
        :param top_n: Number of recommendations to return.
        :type top_n: int
        :return: List of tuples (movie title, similarity score).
        :rtype: list[tuple]
        """
        if selected_features is None or len(selected_features) == 0:
            selected_features = ['genres', 'keywords', 'cast', 'director', 'overview', 'runtime']

        feature_matrix = self.build_matrix(selected_features)

        idx = self.movies[self.movies['title'] == movie_title].index
        if len(idx) == 0:
            return []

        movie_idx = idx[0]
        #We have to make 2D matrix because cosine_simialrity only accept this type of vector
        movie_vector = feature_matrix[movie_idx].reshape(1, -1)

        similarities = cosine_similarity(movie_vector, feature_matrix)[0]
        similar_sorted = similarities.argsort()[::-1]

        recommendations = []
        for index in similar_sorted[1:]:
            found_title = self.movies.iloc[index]['title']
            similarity = similarities[index]
            if similarity==0:
                continue

            recommendations.append((found_title, similarity))
            if len(recommendations) >= top_n:
                break

        return recommendations
