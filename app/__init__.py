from __future__ import print_function, absolute_import, division

import json
import ast
import traceback
from cStringIO import StringIO

from flask import Flask, render_template, Response, request

from toolz import first, curry
from toolz.compatibility import map, zip

from multipledispatch import dispatch

import pandas as pd

from odo import odo
from blaze import Data, compute
from blaze.server import from_tree

import blaze


app = Flask(__name__)


def jsonify(data, status=200, **kwargs):
    return Response(response=json.dumps(data), status=status,
                    **kwargs)


def strtypes(dshape):
    return map(str, dshape.measure.types)


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
    result = [dict(name=field,
                   dshape=dict(pairs=list(map(list, zip(dshape.measure.names,
                                                        strtypes(dshape))))))
              for field, dshape in zip(fields, dshapes)]
    return jsonify(result)


@dispatch(ast.Expression)
def to_json(node, scope=None):
    return to_json(node.body, scope=scope or {})


@dispatch(ast.Name)
def to_json(node, scope=None):
    name = node.id
    if name in scope:
        return {
            'op': 'Symbol',
            'args': [name, scope[name].dshape, None]
        }
    if hasattr(blaze, name.title()):
        return name.title()
    if hasattr(blaze.expr, name):
        return name
    raise NameError(name)


@dispatch(ast.Num)
def to_json(node, scope=None):
    return node.n


@dispatch(ast.Str)
def to_json(node, scope=None):
    return node.s


@dispatch(ast.Call)
def to_json(node, scope=None):
    op = to_json(node.func, scope=scope)
    args = list(map(curry(to_json, scope=scope), node.args))
    if not args:
        raise TypeError('method calls not allowed, '
                        'use the functional form %s(...)' % op)
    return {
        'op': op,
        'args': args
    }


@dispatch(ast.Attribute)
def to_json(node, scope=None):
    return {
        'op': 'Field',
        'args': [to_json(node.value, scope=scope), node.attr]
    }


@app.route('/compute', methods=['POST'])
def compute_from_json():
    data = json.loads(request.data)
    params = data['params']
    if not params:
        return ''
    query = first(params)

    try:
        raw = ast.parse(query, mode='eval')
        js = to_json(raw, scope={'db': db})
        expr = from_tree(js, namespace={'db': db})
        leaf, = expr._leaves()
        expr = expr.head(5) if hasattr(expr, 'head') else expr
        result = repr(Data(compute(expr, {leaf: db.data}), dshape=expr.dshape))
    except Exception:
        sio = StringIO()
        traceback.print_exc(file=sio)
        result = sio.getvalue()
    return jsonify({'output': result})


if __name__ == '__main__':
    db = Data('blaze://localhost:6363')
    app.run(debug=True, port=23532)
