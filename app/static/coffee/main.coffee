require.config
    paths:
        react: '../libs/react/react'
        jquery: '../libs/jquery/dist/jquery'
        bootstrap: '../libs/bootstrap/dist/js/bootstrap'
        'react-bootstrap': '../libs/react-bootstrap/react-bootstrap'
        griddle: '..libs/griddle/build/griddle'

require [
    'react',
    'components/App'
], (React, App) ->
    React.render <App />, document.getElementById('app')
