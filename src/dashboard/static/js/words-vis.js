/**
 * Renders a histogram for selection times
 */
async function render_words_vis(filters = {}) {
    // set the dimensions and margins of the graph
    let margin = { top: 30, right: 60, bottom: 10, left: 60 }
    let width = document.querySelector('#words-vis').offsetWidth
        - margin.left - margin.right
    let height = document.querySelector('#words-vis').offsetHeight
        - margin.top - margin.bottom

    // remove existing svg (if any)
    d3.selectAll("#words-vis > svg").remove()

    // trigger spinner
    /* opts.top = '50px'
    var spinner = new Spinner(opts).spin(document.querySelector('#words-vis')) */

    // fetch data from server
    /* let data = await fetch('http://localhost:8000/get-years-data?'
        + (filters.xKey ? (`xKey=${filters.xKey}&yKey=${filters.yKey}`
            + `&minX=${filters.minX}&minY=${filters.minY}`
            + `&maxX=${filters.maxX}&maxY=${filters.maxY}`) : ''),
        { "credentials": "same-origin" })
        .then(response => response.json()) */
    // use dummy data for now
    let data = [{
        "name": "Apples",
        "value": 10,
    },
    {
        "name": "Bananas",
        "value": 12,
    },
    {
        "name": "Grapes",
        "value": 19,
    },
    {
        "name": "Lemons",
        "value": 25,
    },
    {
        "name": "Limes",
        "value": 36,
    },
    {
        "name": "Oranges",
        "value": 43,
    },
    {
        "name": "Pears",
        "value": 50,
    }]

    // stop spin.js loader
    //  spinner.stop();

    // append the svg object to the relevant div
    var svg = d3.select("#words-vis")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)

    // add axes
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, d3.max(data, d => d.value)])

    let y = d3.scaleBand()
        .domain(data.map(d => d.name))
        .range([height, 0])

    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y).ticks(0))

    let bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("g")

    // append bars
    bars.append("rect")
        .attr("class", "bar")
        .attr('fill', '#69b3a2')
        .attr("y", d => y(d.name))
        .attr("height", y.bandwidth() * 0.9)
        .attr("x", 0)
        .attr("width", d => x(d.value))

    // add a value label to the right of each bar
    bars.append("text")
        .attr("class", "label")
        // y position of the label is halfway down the bar
        .attr("y", d => y(d.name) + y.bandwidth() - 5)
        // x position is 3 pixels to the right of the bar
        .attr("x", d => x(d.value) + 3)
        .text(d => String(d.value).length > 3 ? d3.format("~s")(d.value) : d.value)

    // Add Vis Title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-style", "italic")
        .style("fill", "#505050")
        .text("Distribution of Words in Selected Posts")
}
