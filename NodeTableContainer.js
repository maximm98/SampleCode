import axios from 'axios';
import React from 'react';
import F5App from './index';
import { getLoggedInUser } from '../../../helpers/authUtils';

import { Cookies } from 'react-cookie';
const cookies = new Cookies();
const user = cookies.get('user');
const access_token = user.access;

/*
This holds all state for the microfrontend.
 */
export default class F5 extends React.Component {
    state = {
        nodesData: [],
        chartRef: [],
        conn: [],
        switchstate: [],
        showModal: false,
        showToast: false,
        currentNode: '',
        stateSuccess: false,
        importDisabled: true
    }

    //Initialize microfrontend state. Holds initial state of node data. GET
    componentDidMount() {
        const loggedInUser = getLoggedInUser();

        axios.get('/api/nodes/', {
            params: {
                groups: loggedInUser.groups[0]
            },
            headers: {
                'Authorization': `JWT ${access_token}`
            }

        }).then(res => {

            const nodestate = res.data.map(x => x.nodestate);
            for (var i = 0; i < nodestate.length; i++) {
                if (nodestate[i] === 'up') {

                    nodestate[i] = true;
                }
                else {
                    nodestate[i] = false;
                }
            }
            if (loggedInUser.groups[0] === 'admin') {
                this.setState({ importDisabled: false })
            }
            this.setState({ nodesData: res.data, switchstate: nodestate });
        })


    }
    //state hook for node state switches.
    handleSwitchClick = (e) => {
        this.setState({ showModal: true })
        this.setState({ currentNode: e.target.name.toString() })
    }
    //state hook for node state change confirmation.
    handleModalClose = (e) => {
        this.setState({ showModal: false })
    }
    //state hook for response toast.
    handleToastClose = (e) => {
        this.setState({ showToast: false })
    }

    //state hook that controls/holds state for node states. PATCH
    handleClick = (e) => {
        var indexFound = this.state.nodesData.findIndex(y => y.nodename === this.state.currentNode)
        let nodesData = [...this.state.nodesData];
        let item = { ...nodesData[indexFound] }

        if (item.nodestate === 'up') {
            item.nodestate = 'down'

        }
        else {
            item.nodestate = 'up'
        }

        nodesData[indexFound] = item
        const loggedInUser = getLoggedInUser();
        axios.patch(`/api/nodes/update/${nodesData[indexFound].fqn}/`, { nodestate: nodesData[indexFound].nodestate, groups: loggedInUser.groups[0], username: loggedInUser.username }, {
            params: {
                groups: loggedInUser.groups[0]
            },

            headers: {
                'Authorization': `JWT ${access_token}`
            },

        }).then(res => {
            nodesData[indexFound] = res.data
            this.setState({ nodesData: nodesData, showModal: false, showToast: true, stateSuccess: true })
        }).catch(res => {
            console.log(res)
            this.setState({ stateSuccess: false, showModal: false, showToast: true })
        })
    }
    refreshConnections = (e) => {
        const loggedInUser = getLoggedInUser();

        axios.get('/api/nodes/', {
            params: {
                groups: loggedInUser.groups[0]
            },
            headers: {
                'Authorization': `JWT ${access_token}`
            }

        }).then(res => {
            const nodestate = res.data.map(x => x.nodestate);
            for (var i = 0; i < nodestate.length; i++) {
                if (nodestate[i] === 'up') {

                    nodestate[i] = true;
                }
                else {
                    nodestate[i] = false;
                }
            }
            this.setState({ nodesData: res.data, switchstate: nodestate });
        }).catch(err => {
            console.log(err)
        })
    }
    importData = (e) => {
        const loggedInUser = getLoggedInUser();

        axios.get('/api/nodes/import/', {
            params: {
                groups: loggedInUser.groups[0]
            },
            headers: {
                'Authorization': `JWT ${access_token}`
            }

        }).then(res => {

            const nodestate = res.data.map(x => x.nodestate);
            for (var i = 0; i < nodestate.length; i++) {
                if (nodestate[i] === 'up') {

                    nodestate[i] = true;
                }
                else {
                    nodestate[i] = false;
                }
            }
            this.setState({ nodesData: res.data, switchstate: nodestate });
        }).catch(err => {
            console.log(err)
        })
    }

    render() {

        return (
            <F5App data={this.state.nodesData} handleClick={this.handleClick} refreshConnections={this.refreshConnections} importData={this.importData} handleSwitchClick={this.handleSwitchClick} stateSuccess={this.state.stateSuccess}
                handleToastClose={this.handleToastClose} handleModalClose={this.handleModalClose} showModal={this.state.showModal} showToast={this.state.showToast} importDisabled={this.state.importDisabled} />
        )
    }
}

