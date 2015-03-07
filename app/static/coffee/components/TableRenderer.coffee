define [
    'react'
    'jquery'
    'griddle'
], (React, $, Griddle) ->

    React.createClass
        getDefaultProps: ->
            table: ''

        getInitialState: ->
            results: []

        componentDidMount: ->
            callback = (results) =>
                if @isMounted()
                    @setState
                        results: results
            $.get "/data/#{@props.table}", callback, 'json'
            return

        render: ->
            <Griddle results={@state.results} />
