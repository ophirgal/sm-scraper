/**
 * Renders a histogram for selection times
 */
async function render_words_vis(filters = {}) {

    // remove existing svg (if any)
    d3.selectAll("#words-vis > svg").remove()

    // trigger spinner
    spinner_opts.top = d_select('#words-vis').offsetHeight / 2 + 'px'
    let spinner = new Spinner(spinner_opts).spin(d_select('#words-vis'))
    
    // fetch data from server
    let url = new URL('/get-word-distribution', window.location.origin)
    let params = filters
    
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    let data = await fetch(url, { "credentials": "same-origin" })
    .then(response => response.json())

    // stop spin.js loader
    spinner.stop()

    // set the dimensions and margins of the graph
    let margin = { top: 30, right: 60, bottom: 10, left: 60 }
    let width = document.querySelector('#words-vis').offsetWidth
        - margin.left - margin.right
    let height = data.length * 15
 
    // append a new svg element to the relevant div
    var svg = d3.select("#words-vis")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)

    // add axes
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, d3.max(data, d => d.count)])

    let y = d3.scaleBand()
        .domain(data.map(d => d.word))
        .range([height, 0])

    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y)
                .ticks(0)
                .tickFormat(d => d.length > 10 ? (d.substr(0,8) + '...') : d))

    let bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("g")

    // append bars
    bars.append("rect")
        .attr("class", "bar")
        .attr('fill', '#69b3a2')
        .attr("y", d => y(d.word))
        .attr("height", y.bandwidth() * 0.85)
        .attr("x", 0)
        .attr("width", d => x(d.count))

    // add a value label to the right of each bar
    bars.append("text")
        .attr("class", "label")
        // y position of the label is halfway down the bar
        .attr("y", d => y(d.word) + y.bandwidth() - 5)
        // x position is 3 pixels to the right of the bar
        .attr("x", d => x(d.count) + 3)
        .style("font-size", "12px")
        .text(d => String(d.count).length > 3 ? d3.format("~s")(d.count) : d.count)

    // Add Vis Title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-style", "italic")
        .style("fill", "#505050")
        .text(`Distribution of Words in Results`)
}
