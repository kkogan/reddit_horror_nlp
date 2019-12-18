[👉 Link to Presententation slides](https://drive.google.com/open?id=1-QrHzl9hiH3n7JMZOe3d-prkEt2kSJLWyKU3jY8OwHI)

## Design Draft

#### Question/need: 
What can we uncover about the nature of the horror stories that we tell each other, and how has this changed over time?

#### Description of my sample data:
I used the pushshift.io reddit archive to retrieve every r/NoSleep post between 2010 and November 2019 — roughly 250K posts.

#### Techniques applied
This is an exploration of NLP and unsupervised learning techniques:
 - the scikit-learn, spaCy, nltk, and gensim libraries for things such as bi-gram phrases, lemmatization, stopwords, TFIDF vectorization
 - latent sematic analysis/dimensionality reduction using singular value decomposition, non-negative matrix factorization, and latent Dirichlet allocation. (NMF worked best for me)
 - a bit of practice with Flask and Tableau

#### Future Work
- Improve the topic flask boilerplate UI and deploy it to the cloud instead of just running a local web server.
