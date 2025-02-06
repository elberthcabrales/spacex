<template>
  <div class="min-h-screen bg-black text-white font-space-mono pb-7">
    <!-- Dashboard Title -->
    <h2 class="text-3xl font-bold text-center text-blue-400 py-8">Rocket Insights Dashboard</h2>

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
        <h3 class="text-xl font-semibold text-gray-300 mb-4">Stages</h3>
        <div ref="stagesChart" class="h-64"></div>
      </div>

      <!-- Engines Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">First Stage Engines</h3>
        <div ref="enginesChart" class="h-64"></div>
      </div>

      <!-- Fuel Chart -->
      <div
        class="chart-container bg-gradient-to-br from-gray-900 via-gray-800 to-black rounded-2xl p-6 shadow-2xl border border-gray-700 hover:shadow-3xl transition-shadow duration-300">
        <h3 class="text-xl font-semibold text-gray-300 mb-4">First Stage Fuel (tons)</h3>
        <div ref="fuelChart" class="h-64"></div>
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
      rockets: [
        {
          rocket_name: "Falcon 1",
          active: false,
          weight: "30146",
          height: 22.25,
          diameter: 1.68,
          cost_per_launch: 6700000,
          first_flight: "2006-03-24",
          stages: 2,
          first_stage_reusable: false,
          first_stage_engines: 1,
          first_stage_fuel_amount_tons: 44,
          second_stage_reusable: false,
          second_stage_engines: 1,
          second_stage_fuel_amount_tons: 3,
          total_successful_launches: 2,
          total_upcoming_launches: 0,
          total_failures: 3,
          total_starlinks_deployed: 0,
          total_failures_per_rocket: 3,
        },
        {
          rocket_name: "Falcon 9",
          active: true,
          weight: "549054",
          height: 70,
          diameter: 3.7,
          cost_per_launch: 50000000,
          first_flight: "2010-06-04",
          stages: 2,
          first_stage_reusable: true,
          first_stage_engines: 9,
          first_stage_fuel_amount_tons: 385,
          second_stage_reusable: false,
          second_stage_engines: 1,
          second_stage_fuel_amount_tons: 90,
          total_successful_launches: 3231,
          total_upcoming_launches: 69,
          total_failures: 2,
          total_starlinks_deployed: 3215,
          total_failures_per_rocket: 2,
        },
        {
          rocket_name: "Falcon Heavy",
          active: true,
          weight: "1420788",
          height: 70,
          diameter: 12.2,
          cost_per_launch: 90000000,
          first_flight: "2018-02-06",
          stages: 2,
          first_stage_reusable: true,
          first_stage_engines: 27,
          first_stage_fuel_amount_tons: 1155,
          second_stage_reusable: false,
          second_stage_engines: 1,
          second_stage_fuel_amount_tons: 90,
          total_successful_launches: 3,
          total_upcoming_launches: 2,
          total_failures: 0,
          total_starlinks_deployed: 0,
          total_failures_per_rocket: 0,
        },
        {
          rocket_name: "Starship",
          active: false,
          weight: "1335000",
          height: 118,
          diameter: 9,
          cost_per_launch: 7000000,
          first_flight: "2021-12-01",
          stages: 2,
          first_stage_reusable: true,
          first_stage_engines: 37,
          first_stage_fuel_amount_tons: 3300,
          second_stage_reusable: true,
          second_stage_engines: 6,
          second_stage_fuel_amount_tons: 1200,
          total_successful_launches: 0,
          total_upcoming_launches: 0,
          total_failures: 0,
          total_starlinks_deployed: 0,
          total_failures_per_rocket: 0,
        },
      ],
    };
  },
  mounted() {
    this.drawCostChart();
    this.drawHeightChart();
    this.drawDiameterChart();
    this.drawWeightChart();
    this.drawStagesChart();
    this.drawEnginesChart();
    this.drawFuelChart();
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
      this.drawBarChart("costChart", "", "cost_per_launch", 400, 300, "steelblue");
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
    drawStagesChart() {
      this.drawBarChart("stagesChart", "", "stages", 400, 300, "teal");
    },
    drawEnginesChart() {
      this.drawBarChart("enginesChart", "", "first_stage_engines", 400, 300, "brown");
    },
    drawFuelChart() {
      this.drawBarChart("fuelChart", "", "first_stage_fuel_amount_tons", 400, 300, "red");
    },
    drawLaunchesChart() {
      const margin = { top: 20, right: 30, bottom: 40, left: 90 };
      const width = 400 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3
        .select(this.$refs.launchesChart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3
        .scaleLinear()
        .domain([0, d3.max(this.rockets, (d) => d.total_successful_launches)])
        .range([0, width]);

      const y = d3.scaleBand().domain(this.rockets.map((d) => d.rocket_name)).range([0, height]).padding(0.1);

      svg
        .selectAll(".bar-launches")
        .data(this.rockets)
        .enter()
        .append("rect")
        .attr("class", "bar-launches")
        .attr("x", 0)
        .attr("y", (d) => y(d.rocket_name))
        .attr("width", (d) => x(d.total_successful_launches))
        .attr("height", y.bandwidth())
        .attr("fill", "blue");

      svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
      svg.append("g").call(d3.axisLeft(y));

      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
    },
    drawFailuresChart() {
      const margin = { top: 20, right: 30, bottom: 40, left: 90 };
      const width = 400 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3
        .select(this.$refs.failuresChart)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3.scaleLinear().domain([0, d3.max(this.rockets, (d) => d.total_failures)]).range([0, width]);

      const y = d3.scaleBand().domain(this.rockets.map((d) => d.rocket_name)).range([0, height]).padding(0.1);

      svg
        .selectAll(".bar-failures")
        .data(this.rockets)
        .enter()
        .append("rect")
        .attr("class", "bar-failures")
        .attr("x", 0)
        .attr("y", (d) => y(d.rocket_name))
        .attr("width", (d) => x(d.total_failures))
        .attr("height", y.bandwidth())
        .attr("fill", "maroon");

      svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x));
      svg.append("g").call(d3.axisLeft(y));

      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", -10)
        .attr("text-anchor", "middle")
    },
  },
};
</script>

<style scoped>
/* No custom CSS needed since we're using Tailwind CSS */
</style>