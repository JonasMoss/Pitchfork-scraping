# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 21:21:53 2016

@author: Jonas
"""

from pandas import Series, DataFrame
import pandas as pd
import itertools as it
import seaborn as sns
sns.set(color_codes=True)


genre_table = list(it.chain(*[[(float(review['rating']),review['year'],genre) for genre in review['genres']] 
                               for review in reviews.find({"year":{"$gt":2000}})]))
genre_table = pd.DataFrame(genre_table)
genre_table.columns = ['Rating', 'Year','Genre']
           
genre_means = genre_table.groupby(by=["Year","Genre"]).mean().unstack()
genre_means.plot()

sns.lmplot(x="Year", y="Rating", col="Genre", data=genre_table, palette="Set1",col_wrap=3)

gt = genre_table.groupby(by=["Year","Genre"],as_index=False)

sns.lmplot(x="Year", y="Rating", col="Genre", data=gt.mean(), palette="Set2",col_wrap=3)
sns.lmplot(x="Year", y="Rating", col="Genre", data=gt.var(), palette="Set3",col_wrap=3)


ratings_year = pd.DataFrame([(float(review['rating']),review['year']) for review in reviews.find({"year":{"$gt":2000}})])
ratings_year.columns = ['Rating', 'Year']
sns.distplot(ratings_year.query("Year==2001")["Rating"],bins=20)
sns.distplot(ratings_year.query("Year==2010")["Rating"],bins=20)
sns.distplot(ratings_year.query("Year==2016")["Rating"],bins=20)

sns.distplot(genre_table.query("Year==2015").query("Genre=='Electronic'")["Rating"],bins=20)
sns.distplot(genre_table.query("Year==2015").query("Genre=='Rock'")["Rating"],bins=20)
sns.distplot(genre_table.query("Year==2015").query("Genre=='Rap'")["Rating"],bins=20)

variances = ratings_year.groupby(by="Year").var()
variances["Year"] = variances.index
sns.lmplot(x = "Year", y = "Rating", data = variances)

from scipy.stats import beta
