// @flow
import React from 'react';
import {
    Card,
    CardBody,
} from 'reactstrap';
import { Bar } from 'react-chartjs-2';

/**
  component renders & returns
 the bar chart for node connections within the 
 microfrontend. 
 **/
export default class BarChart extends React.Component {

    render() {
        //define our variables to map node data.
        const arr = this.props.data;
        const conn = arr.map(x => x.currentconnections);
        const nodename = arr.map(v => v.nodename);

        //define our datasets for the chart.
        const barChartData = {
            datasets: []
        };

        var sortPools = arr.reduce(function (r, o) {
            let k = o.poolname;   // unique `poolname` key
            if (r[k] || (r[k] = [])) r[k].push({ poolname: k, nodename: o.nodename, partition: o.partition, ipaddress: o.ipaddress, nodestate: o.nodestate, currentconnections: o.currentconnections });
            return r;
        }, {});

        Object.entries(sortPools).map(([key, value]) => {
            var nodeInfo = [];

            value.forEach(node => {
                nodeInfo.push({ y: node.currentconnections, x: node.nodename })
            })

            barChartData.datasets.push({
                key: key,
                label: key,
                data: nodeInfo,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(54, 100, 255, 0.5)',

                ],
            });
        })

        //define our options for the bar chart.
        const barChartOpts = {
            plugins: {
                legend: {
                    title: {
                        display: true,
                        text: 'Pools',
                        color: 'rgb(241, 93, 34)',
                        font: {
                            size: 20,

                        },
                    },
                    labels: {
                        color: '#aab8c5',
                        font: {
                            size: 13,

                        },
                    },
                },
            },
            scales: {
                x: {
                    stacked: true
                },

                y: {
                    stacked: true
                },

            },
            maintainAspectRatio: false,


        };
        //return the elements.
        return (
            <Card style={{ color: '#f15d22' }}>
                <CardBody>
                    <h4 className="header-title mb-3">Node Connections</h4>

                    <div className="mb-5 mt-4 chartjs-chart" style={{ height: '475px', maxWidth: '100%' }}>
                        <Bar data={barChartData} options={barChartOpts} />
                    </div>
                </CardBody>
            </Card >
        );
    }
}
