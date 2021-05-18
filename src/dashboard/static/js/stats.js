/**
 * Renders statistics at the top of the dashboard
 */
async function render_stats(filters) {
    // fetch stats data from server
    let url = new URL("http://localhost:5000/get-stats")
    let params = filters
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    // fetch data from server
    let stats = await fetch(url, { "credentials": "same-origin" })
        .then(response => response.json())

    document.querySelector('#stat1').innerHTML = `
    <div class="inline left"><strong>Posts Selected:</strong></div>
    <div class="inline right">${d3.format("~s")(stats.posts_selected)}</div>`
    document.querySelector('#stat2').innerHTML = `
        <div class="inline left"><strong>Users Selected:</strong></div>
        <div class="inline right">${d3.format("~s")(stats.users_selected)}</div>`
    document.querySelector('#stat3').innerHTML = `
        <div class="inline left"><strong>Mean Relevance:</strong></div>
        <div class="inline right">${d3.format(".1%")(stats.mean_relevance/100)}</div>`
    document.querySelector('#stat4').innerHTML = `
        <div class="inline left"><strong>Posts Scraped:</strong></div>
        <div class="inline right">${d3.format("~s")(stats.posts_scraped)}</div>`
}

