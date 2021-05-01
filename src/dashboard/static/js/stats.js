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
    <div class="inline left"><strong>Posts selected:</strong></div>
    <div class="inline right">${d3.format("~s")(stats.posts_selected)}</div>`
    document.querySelector('#stat2').innerHTML = `
        <div class="inline left"><strong>Users selected:</strong></div>
        <div class="inline right">${d3.format("~s")(stats.users_selected)}</div>`
    document.querySelector('#stat3').innerHTML = `
        <div class="inline left"><strong>Posts scraped:</strong></div>
        <div class="inline right">${d3.format("~s")(stats.posts_scraped)}</div>`
    document.querySelector('#stat4').innerHTML = `
        <div class="inline left"><strong>Posts relevant:</strong></div>
        <div class="inline right">${d3.format("~s")(stats.posts_relevant)}</div>`
}

