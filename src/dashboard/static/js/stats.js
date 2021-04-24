/**
 * Renders statistics at the top of the dashboard
 */
async function render_stats(filters) {
    // fetch stats data from server
    let url = new URL("http://localhost:5000/get-stats"),
        params = {
            p1: 35.696233,
            p2: 139.570431
        }
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    let stats = await fetch(url, { "credentials": "same-origin" })
        .then(response => response.json())

    console.log('stats', stats)

    document.querySelector('#stat1').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>Posts selected:</strong>&nbsp;${d3.format("~s")(stats.posts_selected)}
        </div>`
    document.querySelector('#stat2').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>Users selected:</strong>&nbsp;${d3.format("~s")(stats.users_selected)}
        </div>`
    document.querySelector('#stat3').innerHTML = `
        <div class="d-flex justify-content-center ">
        <strong>Posts scraped:</strong>&nbsp;${d3.format("~s")(stats.posts_scraped)}
        </div>`
    document.querySelector('#stat4').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>Posts relevant:</strong>&nbsp;${d3.format("~s")(stats.posts_relevant)}
        </div>`
}

