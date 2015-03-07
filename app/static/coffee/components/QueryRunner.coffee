define [
    'react'
    'react-bootstrap'
], (React, ReactBootstrap) ->

    Input = ReactBootstrap.Input

    React.createClass
        getDefaultProps: ->
            renderer: {}

        getInitialState: ->
            query: ''

        render: ->
            renderer = @props.renderer
            <div className="query-runner">
                <form>
                    <Input type="text" label="Run a Blaze query" />
                </form>
                {renderer}
            </div>
