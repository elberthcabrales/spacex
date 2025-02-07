<template>
  <div class="bg-space-gradient min-h-screen p-8 text-white">
    <!-- Dashboard Title -->
    <h2 class="text-3xl font-bold text-center text-blue-400 py-8">Insights</h2>

    <!-- Dashboard Grid -->
    <div class="dashboard grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 container mx-auto ">
      <!-- Cost Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Cost Per Launch ($)</h3>
        <div ref="costChart" class="h-64"></div>
      </div>

      <!-- Height Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Height (m)</h3>
        <div ref="heightChart" class="h-64"></div>
      </div>

      <!-- Diameter Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Diameter (m)</h3>
        <div ref="diameterChart" class="h-64"></div>
      </div>

      <!-- Weight Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Weight (kg)</h3>
        <div ref="weightChart" class="h-64"></div>
      </div>

      <!-- Stages Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">First Stage Engines</h3>
        <div ref="firstStageEnginesChart" class="h-64"></div>
      </div>

      <!-- Engines Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Second Stage Engines</h3>
        <div ref="secondStageEnginesChart" class="h-64"></div>
      </div>

      <!-- Fuel Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Total Upcoming Launches</h3>
        <div ref="totalUpcomingChart" class="h-64"></div>
      </div>

      <!-- Launches Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Total Successful Launches</h3>
        <div ref="launchesChart" class="h-64"></div>
      </div>

      <!-- Failures Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Total Failures</h3>
        <div ref="failuresChart" class="h-64"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "RocketInsights",
  data() {
    return {
      rockets: [], // Data fetched from the API
      loading: true, // Loading state
      error: null, // Error state
    };
  },
  async mounted() {
    const response = await fetch("http://127.0.0.1:8000/api/dashboard/");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    this.rockets = await response.json();
    this.drawCostChart();
    this.drawHeightChart();
    this.drawDiameterChart();
    this.drawWeightChart();
    this.drawFirstStageEnginesChart();
    this.drawSecondStageEnginesChart();
    this.drawTotalUpcomingChart();
    this.drawLaunchesChart();
    this.drawFailuresChart();
  },
  methods: {
    drawBarChart(ref, title, dataKey, width = 400, height = 300, color = "steelblue") {
      const margin = { top: 20, right: 30, bottom: 40, left: 90 };
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const svg = d3
        .select(this.$refs[ref])
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3.scaleLinear().domain([0, d3.max(this.rockets, (d) => +d[dataKey])]).range([0, innerWidth]);
      const y = d3.scaleBand().domain(this.rockets.map((d) => d.rocket_name)).range([0, innerHeight]).padding(0.1);

      svg
        .selectAll(".bar")
        .data(this.rockets)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("y", (d) => y(d.rocket_name))
        .attr("width", (d) => x(+d[dataKey]))
        .attr("height", y.bandwidth())
        .attr("fill", color);

      svg.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(x));
      svg.append("g").call(d3.axisLeft(y));

      svg
        .append("text")
        .attr("x", innerWidth / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
        .text(title);
    },
    drawCostChart() {
      const margin = { top: 20, right: 30, bottom: 40, left: 90 };
      const width = 400 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3
        .select(this.$refs.costChart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3.scaleLinear()
        .domain([0, d3.max(this.rockets, (d) => +d.cost_per_launch)])
        .range([0, width]);

      const y = d3.scaleBand()
        .domain(this.rockets.map((d) => d.rocket_name))
        .range([0, height])
        .padding(0.1);

      // Format numbers for the x-axis (e.g., "7M" for 7,000,000)
      const formatMillions = d3.format(".1s"); // Formats numbers with a single significant digit and SI prefix <button class="citation-flag" data-index="2">
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat((d) => formatMillions(d)));

      svg.append("g").call(d3.axisLeft(y));

      svg.selectAll(".bar")
        .data(this.rockets)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("y", (d) => y(d.rocket_name))
        .attr("width", (d) => x(+d.cost_per_launch))
        .attr("height", y.bandwidth())
        .attr("fill", "steelblue");
    },
    drawHeightChart() {
      this.drawBarChart("heightChart", "", "height", 400, 300, "orange");
    },
    drawDiameterChart() {
      this.drawBarChart("diameterChart", "", "diameter", 400, 300, "green");
    },
    drawWeightChart() {
      this.drawBarChart("weightChart", "", "weight", 400, 300, "purple");
    },
    drawFirstStageEnginesChart() {
      this.drawBarChart("firstStageEnginesChart", "", "first_stage_engines", 400, 300, "teal");
    },
    drawSecondStageEnginesChart() {
      this.drawBarChart("secondStageEnginesChart", "", "second_stage_engines", 400, 300, "brown");
    },
    drawTotalUpcomingChart() {
      this.drawBarChart("totalUpcomingChart", "", "total_upcoming_launches", 400, 300, "red");
    },
    drawLaunchesChart() {
      this.drawBarChart("launchesChart", "", "total_successful_launches", 400, 300, "gold");
    },
    drawFailuresChart() {
      this.drawBarChart("failuresChart", "", "total_failures", 400, 300, "red");
    },
  },
};
</script>

<style scoped>
/* No custom CSS needed since we're using Tailwind CSS */
</style>