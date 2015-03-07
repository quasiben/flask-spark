define [
    'react'
    'jquery'
    'terminal'
], (React, $) ->

    React.createClass
        propTypes:
            parse: React.PropTypes.func

        getDefaultProps: ->
            parse: (query) -> query

        componentDidMount: ->
            self = this
            blaze = ->
                @push(((command, term) ->
                    $.jrpc('/compute', 'blaze', [command],
                           (json) -> term.echo(json.output))
                    return),
                    {prompt: 'blaze> '})
                return
            if @isMounted()
                $(@getDOMNode()).css("overflow: auto")
                $(@getDOMNode()).terminal([{
                    blaze: blaze
                }], {
                        prompt: '> '
                        greetings: 'Welcome to the blaze Terminal, type blaze to begin'
                        height: 400
                    })
        render: ->
            <div />
