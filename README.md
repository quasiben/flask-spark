# flask-spark

**only works on mac os x**

## install

**not for the faint of heart**

* install npm

* install bower and coffee-react from npm
```sh
npm install -g bower
npm install -g coffee-react
```

* `cd` to the repo
* run `bower`

```sh
bower install
```

* install miniconda

* install blaze and co.

```sh
conda install -c blaze blaze
```

## Example

Fire up IPython and start a blaze server
```python
In [2]: import pandas as pd

In [3]: import numpy as np

In [4]: df = pd.DataFrame({'a': np.random.randn(1000),
   ...:                    'b': np.random.randint(0, 10, size=1000)})
   ...:

In [5]: from blaze import Server

In [6]: Server({'db': df}).run(host='127.0.0.1', port=6363)  # <- blocks
```

Fire up two more terminals
* one for the coffee-script jsx watcher
* one for the application

Coffee Script
```sh
cjsx --compile --bare --output app/static/js --watch app/static/coffee
```

Application
```sh
cd wherever/you/cloned/flask-spark
./run.sh
```
