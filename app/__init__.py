from __future__ import print_function

import os
from multiprocessing import Process
from flask import Flask, render_template
from pyspark import SparkContext, HiveContext
from blaze import Server, resource, Data, compute

from toolz.compatibility import map, zip
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<table>', methods=['GET'])
@app.route('/data/<table>/<int:n>', methods=['GET'])
def table(table, n=10):
    return compute(getattr(db, table)).head(n)


@app.route('/data/<table>/columns', methods=['GET'])
def columns(table):
    return list(getattr(db, table).fields)


@app.route('/data/tables', methods=['GET'])
def tables():
    fields = db.fields
    dshapes = map(lambda field: getattr(db, field).dshape, fields)
    return [dict(name=field, dshape=dshape)
            for field, dshape in zip(fields, map(str, dshapes))]


def create_spark_instance():
    return HiveContext(SparkContext('local[*]', 'app'))


def create_blaze_server(sql, data, name, port=4501):
    trip = sql.createDataFrame(pd.DataFrame(data))
    sql.registerDataFrameAsTable(trip, name)
    sql.cacheTable(name)
    db = Server(Data(sql))
    p = Process(target=db.run, kwargs=dict(port=port))
    p.start()
    return p, port


if __name__ == '__main__':
    path = os.path.join(os.path.expanduser('~'),
                        'data', 'trip', 'bcolz', 'all.bcolz')
    assert os.path.exists(path), "%r doesn't exist" % path

    bc = resource(path)
    n = 1000
    sql = create_spark_instance()
    p, port = create_blaze_server(sql, bc[:n], 'trip')
    db = Data('blaze://localhost:%d' % port)
    app.run(debug=True, port=4500)
    p.terminate()
