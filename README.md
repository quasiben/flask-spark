# flask-spark

**only works on mac os x**

## install

**not for the faint of heart**

* install npm

* install bower from npm
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
