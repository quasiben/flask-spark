define [
    'react'
    'react-bootstrap'
    'components/AvailableTables'
    'jquery'
], (React, ReactBootstrap, AvailableTables, $) ->

    PageHeader = ReactBootstrap.PageHeader
    Input = ReactBootstrap.Input
    Row = ReactBootstrap.Row
    Col = ReactBootstrap.Col

    React.createClass
        getInitialState: ->
            output: ""

        translate: (e) ->
            callback = (data) =>
                @setState
                    output: data.result
            $.post '/translate', $('#blaze-query').val(), callback, 'json'

        render: ->
            <div className="content">
                <PageHeader>Translating Spark to <code>Blaze</code></PageHeader>
                <AvailableTables url="/data/tables" />
                <form onInput={@translate}>
                    <Input label="Evaluate a Query" wrapperClassName="wrapper">
                        <Row>
                            <Col xs={6}>
                                <input type="text" id="blaze-query"
                                       className="form-control" />
                            </Col>
                            <Col xs={6}>
                                <output name="q" htmlFor="blaze-query">{@state.output}</output>
                            </Col>
                        </Row>
                    </Input>
                </form>
            </div>
