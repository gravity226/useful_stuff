# NLP Feature importance
In this example we will build a Logistic Regression model to predict whether a user will open an email based on the words in the subject line.  We'll then use the coefficients from the model to determine what words impact the open rate the most.

## Table of Contents
1. [Wrangle your data](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#wrangle-your-data)
2. [Creating the Bag of Words Model](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#creating-the-bag-of-words-model)
3. [Creating the Logistic Regression Model](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#creating-the-logistic-regression-model)
4. [Looking at Feature Importance](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#looking-at-feature-importance)
5. [Making New Predictions](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#making-new-predictions)
6. [Other Thoughts](https://github.com/gravity226/useful_stuff/tree/master/NLP_Feature_Importance#other-thoughts)

## Wrangle your data
I am currently working with an email dataset that shows when an email was delivered and opened.  You can really use anything in this example though as long as you have a piece of text (x) and a response (y):

```
[ ("email subject line 1", 0),
  ("email subject line 2", 1),
  ("email subject line 3", 0) ]
```

In this case my responses are ones and zeros, email opened and not opened.  Every line represents one user that received an email.

## Creating the Bag of Words Model
We first need to convert our data into something useable for the Logistic Regression model.  Enter the Count Vectorizer.  What this does is create a sparse matrix made up of ones and zeros.  Each row in the matrix represents one piece of text (or email subject line in this example) and each column in the row represents one possible word.  

- First we need to build a function to clean up the text before modeling it.  This is a function I've used on a few projects now that removes punctuation, numbers, html, characters and other things.  This is located in a file called clean_text.py.

```Python
import re
import unicodedata
import string

def clean_text(text):
	if text == None:
		return ''

	if isinstance(text, unicode):
		output = text.encode('ascii', 'ignore')
	else:
		output = text.decode('ascii', 'ignore').encode('ascii')

	# remove special characters
	need_to_remove = ['\n', '\t', '&nbsp;', '&rsquo;', '&trade;', '&copy;', '&reg;']
	for r in need_to_remove:
		output = output.replace(r, ' ')

	# remove html
	clean = re.compile('<.*?>')
	output = re.sub(clean, '', output)

	# remove punctuation
	output = output.translate(None, string.punctuation)

	# remove numbers
	output = re.sub(r'[0-9]+', '', output)

	# Remove large groups of spaces
	output = re.sub(' +',' ', output)

	return output.strip().lower()
```

- Next let's grab the distinct values from our dataset and run them through our clean_text function

```Python
from clean_text import clean_text

headlines = [("email subject line 1", 0),
             ("email subject line 2", 1),
             ("email subject line 3", 0)]

results = [ clean_text(r[0]) for r in headlines ]
```

- Now we build the Bag of Words model.  Looking at the parameters in the model, if there's a decode error I want it ignored, I want all stop words in english to be removed, I want to capture a maximum of 1000 features (words), and I want n-grams up to 3.

```Python
from sklearn.feature_extraction.text import CountVectorizer

bow_model = CountVectorizer(decode_error='ignore',
                            stop_words='english',
                            max_features=1000,
                            ngram_range=(1, 3))

bow_model.fit(results)
```

- Now that we have a fitted model, it's a good idea to save it somewhere.

```Python
from sklearn.externals import joblib

joblib.dump(bow_model, 'bow_model_grams.pkl')
```

- So what does this model give us?  Let's see...

```Python
q = bow_model.transform(['email subject line 1'])

print q
# >> <1x1000 sparse matrix of type '<type 'numpy.int64'>' with 1 stored elements in Compressed Sparse Row format>

print q.get_shape()
# >> (1, 1000)
# this tells us that there is 1 row by a 1000 columns, our email headline by the feature space

print q.toarray()
# >> array([[0, 0, 0, 0, ... 0, 0, 0, 0]])
# There's a couple 1's in there somewhere :)
```

## Creating the Logistic Regression Model
Now that we have our Bag of Words created, let's create the Logit model and see how well it fits to our data.

- Creating x and y for our model

```Python
from sklearn.externals import joblib
from clean_text import clean_text

# our data
headlines = [("email subject line 1", 0),
             ("email subject line 2", 1),
             ("email subject line 3", 0)]

# load in our bag of words model
bow_model = joblib.load('bow_model_grams.pkl')

x = [ clean_text(q[0]) for q in headlines ]
x = bow_model.transform(x)

y = [ q[1] if q[1] != None else 0 for q in headlines ]
```

- Fitting the model

```Python
from sklearn.linear_model import LogisticRegression

logit_model = LogisticRegression()
logit_model.fit(x, y)
```

- How well does our model predict the open rate?  

```Python
preds = logit_model.predict(x)

from sklearn.metrics import accuracy_score

print accuracy_score(y, preds)
# >> 0.653316681427
```

- I know what you're thinking... why isn't there a holdout dataset?  Enter K Fold Cross Validation

```Python
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=999)
kf.get_n_splits(x)

acc_scores = []

import numpy as np

y = np.array(y)
for train_index, test_index in kf.split(x):
    X_train, X_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]

    validation_model = LogisticRegression()
    validation_model.fit(X_train, y_train)

    preds = validation_model.predict(X_test)
    acc_scores.append(accuracy_score(y_test, preds))

print sum(acc_scores) / len(acc_scores)
# >> 0.653174939754
```

## Looking at Feature Importance

Now that we have a model that does an ok job of predicting whether a user will open an email let's see how each word / n-gram impacts the model.

```Python
words = zip(bow_model.get_feature_names(), logit_model.coef_[0])

words = sorted(words, key=lambda x: abs(x[1]), reverse=True)

print words[:20]
```

What we're doing here is looking for coefficients that have the highest absolute value for the corresponding n-grams.  This will give us a good idea of what words have the largest positive and negative impact to an email being opened.

```
[(u'just', -3.3146095863688059),
 (u'need know', 3.2354914090316163),
 (u'need help', 2.7018862422065166),
 (u'current', 2.5907121952512266),
 (u'status', 2.5483690954159988),
 (u'leadfirst', -2.4970003950251654),
 (u'teammate', 2.2905605220944798),
 (u'input', 2.2854222408810099),
 (u'business', 2.2080917333530263),
 (u'pulse', -2.0368807754127394),
 (u'tips', -1.9567470835281371),
 (u'fa', 1.9326611488495733),
 (u'release', -1.9090181047752579),
 (u'education', 1.8910581017990298),
 (u'home day', -1.8802073913341524),
 (u'registration', 1.8710203308263464),
 (u'action', 1.8705275022484438),
 (u'spring', -1.8604089717356322),
 (u'email', -1.8288317357137138),
 (u'leadfirst namedefaultedit', 1.8280634097844339)]
```

## Making new Predictions
So could we use this to help create emails that are more likely to be opened?  *Maybe?*

```Python
new_subject_lines = ['Current Status of Business',
                     'Just the tips',
                     'Business Pulse',
                     'Home Day Registration',
                     'Teammate Release Email',
                     'Spring registration tips']

x = [ clean_text(q) for q in new_subject_lines ]
x = bow_model.transform(x)

print logit_model.predict(x)
# >> array([1, 0, 1, 1, 0, 0])
```

Kinda cool right?  The ones and zeros represent whether an email will be opened based on the email subject line.  If you wanted to look a little closer we can also scope out the predicted probability of an open.

```Python
print logit_model.predict_proba(x)
```
```
array([[  8.39022740e-04,   9.99160977e-01],
       [  8.88078218e-01,   1.11921782e-01],
       [  1.53000034e-01,   8.46999966e-01],
       [  9.58613885e-02,   9.04138612e-01],
       [  9.15574255e-01,   8.44257447e-02],
       [  8.57663521e-01,   1.42336479e-01]])
```
What this shows is the probability of a zero or a one showing up ["prob of 0", "prob of 1"].  Looking at these our model seems to be pretty confident in its predictions having greater than a %80 probability in each prediction (one way or the other).  

## Other Thoughts
Even though these results might be interesting we need to remember that this is only giving us a general idea of what's going on.  What might work better would be to add user data to the mix.  Then we could predict at a user level how someone might interact with an email.
