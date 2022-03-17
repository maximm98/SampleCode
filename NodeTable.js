// @flow
import React from 'react';
import {
    Row,
    Col,
    Card,
    CardBody,
} from 'reactstrap';
import BootstrapTable from 'react-bootstrap-table-next';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import ToolkitProvider, { Search, CSVExport } from 'react-bootstrap-table2-toolkit';
import paginationFactory from 'react-bootstrap-table2-paginator';
import Switch from '@material-ui/core/Switch';
/* 
Node Table Component for the microfrontend. 
This component renders & returns a table holding node state.
*/
export default class NodeTable extends React.Component {
    render() {

        //define our static column data.
        const columns =
            [
                {
                    dataField: 'nodename',
                    text: 'Name',
                    sort: true,
                },
                {
                    dataField: 'partition',
                    text: 'Partition',
                    sort: true,
                },
                {
                    dataField: 'vipname',
                    text: 'VIP',
                    sort: false,
                },
                {
                    dataField: 'poolname',
                    text: 'Pool',
                    sort: false,
                },
                {
                    dataField: 'ipaddress',
                    text: 'Address',
                    sort: false,
                },
                {
                    dataField: 'currentconnections',
                    text: 'Current Connections',
                    sort: true,
                },
                {
                    text: 'Node State',
                    dataField: 'nodestate',
                    formatter: (cell, row, index, extra) => {
                        if (cell === 'up') {
                            cell = true
                        }
                        else {
                            cell = false
                        }

                        return (
                            <div>
                                <Switch
                                    checked={cell}
                                    onChange={extra.handleSwitchClick}
                                    name={row.nodename}
                                    inputProps={{ 'aria-label': 'secondary checkbox' }}
                                />
                                <Modal show={extra.showModal} onHide={extra.handleModalClose}>
                                    <Modal.Header closeButton>
                                        <Modal.Title>Node State Change Confirmation</Modal.Title>
                                    </Modal.Header>
                                    <Modal.Body>Are you sure you want to update the state of this node?</Modal.Body>
                                    <Modal.Footer>
                                        <Button variant="secondary" onClick={extra.handleModalClose}>
                                            No
                                        </Button>
                                        <Button variant="primary" onClick={extra.handle} name={row.nodename}>
                                            Yes
                                        </Button>
                                    </Modal.Footer>
                                </Modal>

                            </div>
                        )
                    },
                    formatExtraData: { handle: this.props.handleClick, handleSwitchClick: this.props.handleSwitchClick, handleModalClose: this.props.handleModalClose, showModal: this.props.showModal }
                },
            ]
        //define our sort defaults.
        const defaultSorted = [
            {
                dataField: 'id',
                order: 'asc',
            },
        ]
        //instantiate our Search & CSVExport components.
        const { SearchBar } = Search;
        const { ExportCSVButton } = CSVExport;

        //return component elements.
        return (
            <Card>
                <CardBody >
                    <h2 className="header-title" style={{ color: "#f15d22" }}>F5 Nodes</h2>

                    <ToolkitProvider
                        bootstrap4
                        keyField="fqn"
                        data={this.props.data}
                        columns={columns}
                        columnToggle
                        search
                        exportCSV={{ onlyExportFiltered: true, exportAll: false }}>
                        {props => (
                            <React.Fragment>
                                <Row >
                                    <Col>
                                        <SearchBar {...props.searchProps} />

                                    </Col>
                                    <Col className="col-sm-auto">
                                        <Button onClick={this.props.importData} className="btn btn-primary" disabled={this.props.importDisabled}>
                                            Data Import
                                        </Button>

                                    </Col>
                                    <Col className="col-sm-auto">
                                        <Button onClick={this.props.refreshConnections} className="btn btn-primary">
                                            Refresh
                                        </Button>

                                    </Col>

                                    <Col className="col-md-auto">
                                        <ExportCSVButton {...props.csvProps} className="btn btn-primary">
                                            Export CSV
                                        </ExportCSVButton>

                                    </Col>
                                </Row>

                                <BootstrapTable
                                    {...props.baseProps}
                                    bordered={false}
                                    defaultSorted={defaultSorted}
                                    pagination={paginationFactory({ sizePerPage: 5 })}
                                    // selectRow={selectRow}
                                    wrapperClasses="table-responsive"
                                />
                            </React.Fragment>
                        )}
                    </ToolkitProvider>
                </CardBody>
            </Card>
        );
    };



}


