# Using Python 2.7 with Looker
Getting familiar with the Looker Python api and using Python to create Looker Looks with a little data science goodness mixed in.

## Table of Contents
1. [Download the Looker API](https://github.com/gravity226/looker_python#download-the-looker-api)
2. [Getting Familiar with the API](https://github.com/gravity226/looker_python#getting-familiar-with-the-api)
    - [Setting up your client](https://github.com/gravity226/looker_python#setting-up-your-client)
    - [Inline Queries](https://github.com/gravity226/looker_python#inline-query)
    - [Models](https://github.com/gravity226/looker_python#models)
    - [Looks](https://github.com/gravity226/looker_python#looks)
3. [Use Case](https://github.com/gravity226/looker_python#use-case)
    - [Get some data for the regression model](https://github.com/gravity226/looker_python#get-some-data-to-build-the-regression-model)
    - [Creating the Query](https://github.com/gravity226/looker_python#creating-the-query)
    - [Creating the Look](https://github.com/gravity226/looker_python#creating-the-look)
4. [Other Thoughts](https://github.com/gravity226/looker_python#other-thoughts)
5. [Conclusion?](https://github.com/gravity226/looker_python#conclusion)
6. [References](https://github.com/gravity226/looker_python#references)

## Download the Looker API
This Looker Discourse has a great article on [generating the python API](https://discourse.looker.com/t/generating-client-sdks-for-the-looker-api/3185).  When cloning the repo I had to put in the full URL instead of the git@github...  At the end I also didn't move the folder to a new folder called looker because I already have a python library called looker.  You'll see in the code that I reference this instead:

```Python
import swagger_client as looker
```

## Getting Familiar with the API
#### Setting up your client
Save this in a file called get_client.py.  You'll see this used in every example here.
```Python
import os
import swagger_client as looker

def get_client():
    # base_url = "https://<instance>.looker.com:19999/api/3.0/"
    base_url = os.environ['LOOKER_BASE_URL']
    client_id = os.environ['LOOKER_CLIENT_ID']
    client_secret = os.environ['LOOKER_CLIENT_SECRET']

    # instantiate Auth API
    unauthenticated_client = looker.ApiClient(base_url)
    unauthenticated_authApi = looker.ApiAuthApi(unauthenticated_client)

    # authenticate client
    token = unauthenticated_authApi.login(client_id=client_id, client_secret=client_secret)
    client = looker.ApiClient(base_url, 'Authorization', 'token ' + token.access_token)

    return client
```

#### Inline Query
Queries can be created, run, destroyed, and run inline.  This example shows running a query inline.  We'll create a query in the use case below.  

```Python
import ast
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/query
query = looker.QueryApi(client)

body = {}
body['model'] = 'my_looker_model'
body['view'] = 'my_view'
body['limit'] = '1000'
body['fields'] = ['view1.dimension1', 'view1.measure1']

results = query.run_inline_query(result_format='json', body=body)

r = ast.literal_eval(results)

print r
```

#### Models
- Getting all models.
```Python
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/lookml-model
models = looker.LookmlModelApi(client)

all_models = models.all_lookml_models()

print all_models
```

- Creating a model
```Python
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/lookml-model
models = looker.LookmlModelApi(client)

body = {}
body['name'] = 'tommys_model'
body['project_name'] = 'my_project'
body['allowed_db_connection_names'] = ['db_connect']
body['label'] = 'tommys_test'

new_model = models.create_lookml_model(body=body)
```

- Updating a model
``` Python
import ast
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/lookml-model
models = looker.LookmlModelApi(client)

body = {}
body['has_content'] = True

lookml_model_name = 'tommys_model'

updated_model = models.update_lookml_model(lookml_model_name, body)
```

- Deleting a model
```Python
import ast
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/lookml-model
models = looker.LookmlModelApi(client)

lookml_model_name = 'tommys_model'

models.delete_lookml_model(lookml_model_name)
```

#### Looks
We'll go into more detail on Looks in the next section.

- Get all looks
```Python
import swagger_client as looker
from get_client import get_client

client = get_client()

# https://docs.looker.com/reference/api-and-integration/api-reference/lookml-model
looks = looker.LookApi(client)

all_looks = looks.all_looks()

print all_looks
```

## Use Case
We want to build a Look that shows **click through rate** on the y axis and **email word count** and on x asis.  Then we want to draw a regression line through the dataset.

#### Get some data to build the regression model
```Python
import swagger_client as looker
from get_client import get_client
import ast

client = get_client()
query = looker.QueryApi(client)

body = {}
body['model'] = 'my_looker_model'
body['view'] = 'my_view'
body['limit'] = '1000'
body['fields'] = ['view1.word_count', 'view2.click_through_rate']

results = query.run_inline_query(result_format='json', body=body)

r = ast.literal_eval(results)

# did you get the results you were expecting?
print r[:10]

from sklearn.linear_model import LinearRegression

x = [ [q['view1.word_count']] if q['view1.word_count'] != None else [0] for q in r ]
y = [ q['view2.click_through_rate'] for q in r ]

model =  LinearRegression()

model.fit(x, y)
```

Do you remember back in your high school geometry class when you learned y = mx +b?  Well we're going to use that here (whether you remember it or not).  In this case our y will be our predicted value, our x will be the word count, the m or the slope will be the first coefficient, and the b will be the intercept.  A little more data sciency way to write this would be:
<br />

y&#770; = &beta;<sub>0</sub> + &beta;<sub>1</sub> * x<sub>1</sub> ...
<br />

So let's get our intercept and coefficient from the model we just built.  With those we can calculate the predicted value for y and plot it.
```Python
print model.intercept_
print model.coef_[0]
```

#### Creating the query
Looker needs to store the query that you're going to use for the Look.  The query also holds that visualization config that the Look will use.

- imports and client
```Python
import swagger_client as looker
from get_client import get_client
import json
import ast

client = get_client()
```

- define the basic structure for the query
```Python
body = {}
body['model'] = 'my_looker_model'
body['view'] = 'my_view'
body['limit'] = '500'

# in this case the word_count is a dimension and the crt is a measure.  This is import for the vis to display properly
body['fields'] = ['view1.word_count', 'view1.click_through_rate']
```

- define the vis_config (it's a line chart, it has grid lines...)
```Python
vis_config = {u'hidden_fields': None,
              u'interpolation': 'linear',
              u'label_density': '25',
              u'legend_position': 'center',
              u'limit_displayed_rows': 'False',
              u'point_style': 'none',
              u'show_null_points': 'True',
              u'show_value_labels': 'False',
              u'show_view_names': 'True',
              u'show_x_axis_label': 'True',
              u'show_x_axis_ticks': 'True',
              u'show_y_axis_labels': 'True',
              u'show_y_axis_ticks': 'True',
              u'stacking': '',
              u'type': 'looker_line',
              u'x_axis_gridlines': 'False',
              u'x_axis_scale': 'auto',
              u'y_axis_combined': 'True',
              u'y_axis_gridlines': 'True',
              u'y_axis_scale_mode': 'linear',
              u'y_axis_tick_density': 'default',
              u'y_axis_tick_density_custom': '5'}

body['vis_config'] = vis_config
```

- define any filters, or not (I don't want to see a click through rate greater than 1, because... why are there rates greater than 1?)
```Python
body['filters'] = {u'view1.click_through_rate': '<1'}
```

- define the table calc for the regression line.  Don't forget to replace the numbers with your coefficient and intercept: **word_count * coef_ + intercept_**  Notice how I've also added the **+ (${view2.click_through_rate} * 0)** to the equation.  This is so the regression line will be plotted on the correct axis.  By default Looker tries to plot any dimension (and its table calc) on the x axis and any measure on the y axis.  So by adding our measure to the calculation the line will plot correctly.
```Python
dynamic_fields = [ { u'_kind_hint': u'measure',
                     u'_type_hint': u'number',
                     u'expression': u'${view1.word_count} * -0.0000065456 + 0.062773587493323471 + (${view2.click_through_rate} * 0)',
                     u'label': u'y_pred',
                     u'table_calculation': u'y_pred',
                     u'value_format': None,
                     u'value_format_name': None } ]

# Looker is picky about how it reads json... So let's remove some spaces, but not all of them :)
text = json.dumps(dynamic_fields).replace(', ', ',').replace(': ', ':')

body['dynamic_fields'] = text
```

- create the query
```Python
new_query = query.create_query(body=body)
```

- did you want to check the results of the query?  You should see both fields and the table calc.
```Python
results = query.run_query(query_id=new_query.id, result_format='json')
r = ast.literal_eval(results)

print r[0]
```

#### Creating the look
```Python
body = {}
body['model'] = {'can': None, 'id': 'davita_comms_qa', 'label': 'Davita Comms Qa'}
body['space_id'] = '7'
body['title'] = 'test creating a look'
body['query_id'] = new_query.id

new_look = looks.create_look(body=body)
```

- check out your new look => https://\<instance\>.looker.com/looks/look_id
```Python
print new_look.id
```

## Other Thoughts
The Looker API isn't perfect.  I found a couple bugs working with it and reported them to Looker.  Just keep in mind that you may need to do some adjustments to your Looks after you create them with Python.

## Conclusion?
There are many other use cases for python and looker out there.  If you have an example that you would like to share with the world, feel free to create a pull request and add it in.  Also feel free to create a pull request for any errors you might find.

## References

- Your Looker API URL (https://\<instance\>.looker.com:19999/api/3.0/)

- [Looker Discourse => Generating the python API](https://discourse.looker.com/t/generating-client-sdks-for-the-looker-api/3185)

- [Swagger Code Generator GitHub](https://github.com/swagger-api/swagger-codegen)
