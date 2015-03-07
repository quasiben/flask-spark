define [
    'react'
    'react-bootstrap'
    'jquery'
], (React, ReactBootstrap, $) ->

    Table = ReactBootstrap.Table

    React.createClass
        componentWillMount: ->
            callback = (data) =>
                @setState
                    tables: data
                    loading: false
                return

            $.get @props.url, callback, 'json'
            return

        getInitialState: ->
            tables: []
            loading: true

        getFullTable: ->
            body = @state.tables.map (row, i) ->
                <tr key={i}>
                    <td key={i}>{row.name}</td>
                    <td key={i + 1}>{row.dshape}</td>
                </tr>
            <Table striped bordered condensed hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>DataShape</th>
                    </tr>
                </thead>
                <tbody>
                    {body}
                </tbody>
            </Table>

        render: ->
            if not @state.loading then
                @getFullTable()
            else
                <div />
