/**
 * Renders a histogram for selection times
 */
async function render_times_vis(filters = {}) {

    // set the dimensions and margins of the graph
    let margin = { top: 35, right: 25, bottom: 20, left: 30 }
    let width = document.querySelector('#times-vis').offsetWidth
        - margin.left - margin.right
    let height = document.querySelector('#times-vis').offsetHeight
        - margin.top - margin.bottom

    // remove existing svg (if any)
    d3.selectAll("#times-vis > svg").remove()

    // make sure date inputs are valid and if not display "N/A"
    if (new Date(dateRange.min) >= new Date(dateRange.max)) {
        // append the svg object to the relevant div
        var svg = d3.select("#times-vis")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr('fill', '#4f4f4f')
            .attr("transform", `translate(${margin.left}, ${margin.top})`)

        // Add Vis Title
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", (height / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("font-style", "italic")
            .style("fill", "#505050")
            .text("N/A")

        return
    }

    // trigger spinner
    /* opts.top = '50px'
    var spinner = new Spinner(opts).spin(document.querySelector('#times-vis')) */

    /* let url = new URL("http://localhost:5000/get-date-histogram"),
        params = {
            minDate: d3.timeFormat('%Y-%m-%d %H:%M:%S')(dateRange.min),
            maxDate: d3.timeFormat('%Y-%m-%d %H:%M:%S')(dateRange.max),
            totalBins: 5
        }
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    // fetch data from server
    let data = await fetch(url, { "credentials": "same-origin" })
        .then(response => response.json())

    data = d3.map(data, d => {
        return {
            binMin: new Date(d.binMin).getTime(),
            binMax: new Date(d.binMax).getTime(),
            count: d.count
        }
    })

    data = {
        minDate: dateRange.min,
        maxDate: dateRange.max,
        maxCount: d3.max(d3.map(data, d => d.count)),
        data: data
    } */

    let data = {
        minDate: 770452120500,
        maxDate: 879250032000,
        maxCount: 25,
        data: [
            { binMin: 770452120500, binMax: 792211702800, count: 5 },
            { binMin: 792211702800, binMax: 813971285100, count: 15 },
            { binMin: 813971285100, binMax: 835730867400, count: 25 },
            { binMin: 835730867400, binMax: 857490449700, count: 20 },
            { binMin: 857490449700, binMax: 879250032000, count: 25 }
        ]
    }

    // stop spin.js loader
    //  spinner.stop();

    // append the svg object to the relevant div
    var svg = d3.select("#times-vis")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr('fill', '#4f4f4f')
        .attr("transform", `translate(${margin.left}, ${margin.top})`)

    // Add X axis
    var x = d3.scaleLinear()
        .domain([data.minDate, data.maxDate])
        .range([0, width])

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .attr("class", "x-axis")
        .call(d3.axisBottom(x)
            .tickFormat((_, i) => {
                return d3.timeFormat("%b '%y")(data.data[i].binMin) + '-'
                    + d3.timeFormat("%b '%y")(data.data[i].binMax)
            })
            .ticks(data.data.length))
        .selectAll(".tick")
        .attr("transform", (d, i) => `translate(${x(d) + 5 + i * 7}, 0)`)
        .attr("font-size", "6pt")
    /* .selectAll("text")
    .each(insertLinebreaks) */

    // add x-axis label
    svg.append("text")
        .attr("y", height + margin.bottom / 1.35)
        .attr("x", width / 2)
        .style("text-anchor", "middle")
    // .text("date")

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, data.maxCount])
        .range([height, 0])

    svg.append("g")
        .call(d3.axisLeft(y)
            .ticks(5)
            .tickFormat((d, i) => String(d).length > 3 ? d3.format("~s")(d) : d)
        )

    // add y-axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left / 1.5)
        .attr("x", -height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
    // .text('count')

    // append the bar rectangles to the svg element
    svg.selectAll("rect")
        .data(data.data)
        .enter()
        .append("rect")
        .attr("transform", d => `translate(${x(d.binMin)}, ${y(d.count)})`)
        .attr("width", d => Math.max(x(d.binMax) - x(d.binMin) - 1, 0))
        .attr("height", d => Math.max(height - y(d.count), 0))
        .style("fill", "#4282c2")

    // Add Vis Title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-style", "italic")
        .style("fill", "#505050")
        .text("Histogram of Selected Posts by Date");

    // remove old plots while still there
    while (d3.selectAll("#times-vis > svg")['_groups'][0].length > 1)
        d3.select("#times-vis > svg").remove()
}
