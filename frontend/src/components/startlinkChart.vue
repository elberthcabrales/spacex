<template>
    <div>
        <h1>Starlink Launches Over Time</h1>
        <svg ref="chart" width="800" height="400"></svg>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    data() {
        return {
            starlinkLaunches: [
                { rocket: "Falcon 9", id: "5eefa85e6527ee0006dcee24", mission: "STARLINK-46", date: "2020-02-20T21:36:25", payload: "STARLINK-46" },
                { rocket: "Falcon 9", id: "5eefa8646527ee0006dcef63", mission: "STARLINK-1220", date: "2020-03-09T22:46:17", payload: "STARLINK-1220" },
                { rocket: "Falcon 9", id: "5eefa8636527ee0006dceea5", mission: "STARLINK-1118", date: "2020-04-02T18:11:05", payload: "STARLINK-1118" },
                { rocket: "Falcon 9", id: "5eed7714096e59000698563b", mission: "STARLINK-67", date: "2020-05-27T09:56:08", payload: "STARLINK-67" },
                { rocket: "Falcon 9", id: "5eed7715096e5900069856fe", mission: "STARLINK-1087", date: "2020-05-29T07:06:09", payload: "STARLINK-1087" },
                { rocket: "Falcon 9", id: "5eed7716096e5900069857c9", mission: "STARLINK-1440", date: "2020-07-14T14:56:08", payload: "STARLINK-1440" },
                { rocket: "Falcon 9", id: "5eed770f096e590006985617", mission: "TINTIN B", date: "2020-08-08T05:36:08", payload: "TINTIN B" },
                { rocket: "Falcon 9", id: "5eed7714096e590006985636", mission: "STARLINK-41", date: "2020-08-09T09:26:08", payload: "STARLINK-41" },
                { rocket: "Falcon 9", id: "5eed770f096e590006985612", mission: "STARLINK-22", date: "2020-08-09T19:11:44", payload: "STARLINK-22" },
                { rocket: "Falcon 9", id: "5eed7714096e590006985622", mission: "STARLINK-66", date: "2020-08-21T05:26:09", payload: "STARLINK-66" }
            ]
        };
    },
    mounted() {
        this.createChart();
    },
    methods: {
        createChart() {
            const svg = d3.select(this.$refs.chart);
            const margin = { top: 40, right: 30, bottom: 70, left: 100 };
            const width = +svg.attr('width') - margin.left - margin.right;
            const height = +svg.attr('height') - margin.top - margin.bottom;

            // Parse dates
            const parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%S");
            this.starlinkLaunches.forEach(d => d.date = parseDate(d.date));

            // Set up scales
            const x = d3.scaleTime()
                .domain(d3.extent(this.starlinkLaunches, d => d.date))
                .range([0, width]);

            const y = d3.scalePoint()
                .domain(this.starlinkLaunches.map(d => d.mission))
                .range([0, height])
                .padding(0.5);

            // Create the chart group
            const g = svg.append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            // Add X axis
            g.append('g')
                .attr('transform', `translate(0,${height})`)
                .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat("%Y-%m-%d")));

            // Add Y axis
            g.append('g')
                .call(d3.axisLeft(y));

            // Add dots for each launch
            g.selectAll('.dot')
                .data(this.starlinkLaunches)
                .enter().append('circle')
                .attr('class', 'dot')
                .attr('cx', d => x(d.date))
                .attr('cy', d => y(d.mission))
                .attr('r', 5)
                .attr('fill', 'steelblue');

            // Add labels for each dot
            g.selectAll('.label')
                .data(this.starlinkLaunches)
                .enter().append('text')
                .attr('class', 'label')
                .attr('x', d => x(d.date) + 10)
                .attr('y', d => y(d.mission) + 4)
                .text(d => d.payload)
                .style('font-size', '10px')
                .style('fill', '#333');
        }
    }
};
</script>

<style>
.dot {
    fill: steelblue;
    stroke: #fff;
    stroke-width: 1.5px;
}

.label {
    font-size: 12px;
    fill: black;
}
</style>