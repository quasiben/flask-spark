define [
    'react'
    'react-bootstrap'
    'components/AvailableTables'
    'jquery'
    'components/Terminal',
], (React, ReactBootstrap, AvailableTables, $, Terminal) ->

    PageHeader = ReactBootstrap.PageHeader

    React.createClass
        render: ->
            <div className="content">
                <PageHeader>Blaze Terminal</PageHeader>
                <Terminal />
                <AvailableTables url="/data/tables" />
            </div>
