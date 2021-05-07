/**
 * Renders a histogram for selection times
 */
async function render_times_vis(filters = {}) {

    function remove_old_plots() {
        // remove old plots while still there
        while (d3.selectAll("#times-vis > svg")['_groups'][0].length > 1)
            d3.select("#times-vis > svg").remove()
    }

    // set the dimensions and margins of the graph
    let margin = { top: 35, right: 25, bottom: 10, left: 30 }
    let width = d_select('#times-vis').offsetWidth - margin.left - margin.right
    let height = d_select('#times-vis').offsetHeight - margin.top - margin.bottom

    function displayNA() {
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
            .attr("y", 0 - (margin.top / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("font-style", "italic")
            .style("fill", "#505050")
            .text(`Histogram of Results by Date`)

        // Add N/A text
        svg.append("text")
            .attr("x", (width / 2))
            .attr("y", (height / 2))
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("font-style", "italic")
            .style("fill", "#505050")
            .text("N/A")

        remove_old_plots()
    }

    // remove existing svg (if any)
    d3.selectAll("#times-vis > svg").remove()

    // if date inputs are invalid display "N/A"
    if (new Date(dateRange.min) >= new Date(dateRange.max)) {
        displayNA()
        return
    }

    // trigger spinner
    spinner_opts.top = d_select('#times-vis').offsetHeight / 2 + 'px'
    let spinner = new Spinner(spinner_opts).spin(d_select('#times-vis'))

    // fetch data from server
    let url = new URL('/get-date-histogram', window.location.origin)
    let params = filters
    params.minDate = d3.timeFormat('%Y-%m-%d %H:%M:%S')(dateRange.min)
    params.maxDate = d3.timeFormat('%Y-%m-%d %H:%M:%S')(dateRange.max)
    params.totalBins = 5
    params.resolution = d_select('.hist-btn.btn-primary').innerText

    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    var data = await fetch(url, { "credentials": "same-origin" })
        .then(response => response.json())

    // stop spin.js loader
    spinner.stop()

    // if data is empty display "N/A"
    if (data.length === 0) {
        displayNA()
        return
    }

    data = d3.map(data, d => {
        return {
            binMin: new Date(d.binMin).getTime(),
            binMax: new Date(d.binMax).getTime(),
            count: d.count
        }
    })

    data = {
        minDate: data[0].binMin,
        maxDate: data[data.length - 1].binMax,
        maxCount: d3.max(d3.map(data, d => d.count)),
        data: data
    }

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
            .tickFormat((d, i) => {
                let tick = ''
                try {
                    tick = d3.timeFormat("%b '%y")(data.data[i].binMin) + '-'
                        + d3.timeFormat("%b '%y")(data.data[i].binMax)
                } catch (err) {
                    return ""
                }
                return tick
            })
            .ticks(0))
        .selectAll(".tick")
        .attr("transform", (d, i) => `translate(${x(d) + 5 + i * 7}, 0)`)
        .attr("font-size", "6pt")

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

    // add the Y-axis gridlines
    svg.append("g")
        .attr("class", "grid")
        .attr('color', 'rgba(0,0,0,0.1)')
        .call(d3.axisLeft(y)
            .ticks(5)
            .tickSize(-width)
            .tickFormat("")
        )

    // add y-axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left / 1.5)
        .attr("x", -height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")

    // tooltip div
    var hist_tooltip = svg
        .append("text")
        .attr("class", "hist-tooltip")
        .attr("text-anchor", "middle")
        .style("font-size", "10px")
        .style("font-weight", "bold")
        .style("opacity", 0)

    // append the bar rectangles to the svg element
    svg.selectAll("rect")
        .data(data.data)
        .enter()
        .append("rect")
        .attr("transform", d => `translate(${x(d.binMin)}, ${y(d.count)})`)
        .attr("width", d => Math.max(x(d.binMax) - x(d.binMin) - 1, 0))
        .attr("height", d => Math.max(height - y(d.count), 0))
        .style("fill", "#4282c2")
        .on('mouseover', (evt, d) => {
            let hist_tooltip_node = d_select('.hist-tooltip')
            // bring tooltip to front
            hist_tooltip_node.parentElement.appendChild(hist_tooltip_node)
            d3.select(evt.target).attr('opacity', '.70')
            hist_tooltip.style("opacity", 1)
            let description = d3.timeFormat("%m-%d-%Y")(d.binMin)
            hist_tooltip
                .text(description)
                .attr("x", x(d.binMin))
                .attr("y", y(d.count) - 3)
       })
       .on('mouseout', (evt, d) => {
            d3.select(evt.target).attr('opacity', '1')
            hist_tooltip.style("opacity", 0)
       })
        

    // Add Vis Title
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("font-style", "italic")
        .style("fill", "#505050")
        .text(`Histogram of Results by ${getHistogramResolution()}`)

    remove_old_plots()
}

function getHistogramResolution() {
    let resolutionDict = {
        '1D': 'Days', '1W': 'Weeks', '1M': 'Months',
        '3M': '3 Months', '1Y': 'Years'
    }
    return resolutionDict[d_select('.hist-btn.btn-primary').innerText]
}


// handler for resolution button clicks ('1D', '1M', ...)
function histBtnClicked(e) {
    // change old selection
    let oldBtn = d_select('.hist-btn.btn-primary')
    oldBtn.classList.remove("btn-primary")
    oldBtn.classList.add("btn-light")
    // change new selection
    let newBtn = e.target
    newBtn.classList.remove("btn-light")
    newBtn.classList.add("btn-primary")
    renderAll(false, true, false, false)
}
