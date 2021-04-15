/**
 * Renders a histogram for selection times
 */
async function render_times_vis(filters = {}) {
    // set the dimensions and margins of the graph
    let margin = { top: 35, right: 35, bottom: 30, left: 30 }
    let width = document.querySelector('#times-vis').offsetWidth
        - margin.left - margin.right
    let height = document.querySelector('#times-vis').offsetHeight
        - margin.top - margin.bottom
    
    // remove existing svg (if any)
    d3.selectAll("#times-vis > svg").remove()

    // trigger spinner
    /* opts.top = '50px'
    var spinner = new Spinner(opts).spin(document.querySelector('#times-vis')) */

    // fetch data from server
    /* let data = await fetch('http://localhost:8000/get-years-data?'
        + (filters.xKey ? (`xKey=${filters.xKey}&yKey=${filters.yKey}`
            + `&minX=${filters.minX}&minY=${filters.minY}`
            + `&maxX=${filters.maxX}&maxY=${filters.maxY}`) : ''),
        { "credentials": "same-origin" })
        .then(response => response.json()) */
    // use dummy data for now
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

    /* function insertLinebreaks(d) {
        var el = d3.select(this)
        var words = el._groups[0][0].textContent.split('-')
        el.text('')
        for (var i = 0; i < words.length; i++) {
            let word = words[i]
            var tspan = el.append('tspan').text(word + '-') 
            if (i > 0) tspan.attr('x', 0).attr('dy', '1em')
        }
    } */

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
        .text("Distribution of Selected Posts by Date");

    //////////////////////        BRUSH CODE      ///////////////////////////
    /* // define brush
    let brush = d3.brushX()
        .extent([[margin.left, margin.top], [margin.left + width, margin.top + height]])
        .on("brush", brushing)
        .on('end', brush_end)
 
    // event handle for brushing
    function brushing(event) {
        if (!event.sourceEvent) return; // Only transition after input.
        if (!event.selection) return; // Ignore empty yearSelections
 
        yearSelection = d3.brushSelection(this)
        d3.selectAll('#times-vis svg g rect')
            .style('fill', d => x(d.binMin) + margin.left >= yearSelection[0]
                && x(d.binMax) + margin.left <= yearSelection[1] + 5 ? '#4282c2' : 'gray')
 
        // snap to quantized values
        d3.select("#times-vis svg")
            .call(event.target.move, yearSelection.map(d => x(Math.round(x.invert(d))) + 4))
    }
 
    function brush_end(event) {
        if (!event.sourceEvent) return; // Only transition after input.
        if (!event.selection) return; // Ignore empty yearSelections
        yearSelection = d3.brushSelection(this)
        let selected_years = yearSelection
            .map(d => Math.round(x.invert(d - margin.left)))
 
        // perform cross-filtering
        // only update other charts based on visible changes
        if (!event.target.lastSelection
            || event.target.lastSelection[0] !== selected_years[0]
            || event.target.lastSelection[1] !== selected_years[1]) {
            event.target.lastSelection = selected_years
            filters.minYear = selected_years[0]
            filters.maxYear = selected_years[1]
            render_all(true, true, false, true, filters) // render all but self
        }
    }
 
    // add event listener for reset btn
    document.querySelector('#reset-years-btn').onclick = e => {
        yearSelection = filters.minYear = filters.maxYear = null
        brush.clear(d3.select("#times-vis svg"))
        d3.selectAll('#times-vis svg g rect').style('fill', '#4282c2')
        render_all(true, true, false, true, filters) // render all but self
    }
 
    // Add brushing
    d3.select("#times-vis svg")
        .call(brush)
 
    // move to existing selection (if any)
    if (yearSelection) {
        d3.selectAll('#times-vis svg g rect')
            .style('fill', d => x(d.binMin) + margin.left >= yearSelection[0]
                && x(d.binMax) + margin.left <= yearSelection[1] + 7 ? '#4282c2' : 'gray')
 
        d3.select("#times-vis svg")
            .call(brush.move, yearSelection.map(d => x(Math.round(x.invert(d))) + 4))
    } */
}
