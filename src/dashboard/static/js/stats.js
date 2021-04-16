/**
 * Renders statistics at the top of the dashboard
 */
function render_stats(filters) {
    // fetch stats data from server
    // let data = await fetch(...)
    
    // use dummy data for now
    let total_selected = 120 // Total posts filtered/selected
    let total_unique_users = 35 // Total unique users in selection
    let total_scraped = 25000 // Total posts scraped
    let total_relevant = 2500 // Total posts relevant (out of all scraped?)

    document.querySelector('#stat1').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>No. posts selected:</strong>&nbsp;${Number(total_selected).toLocaleString()}
        </div>`
        document.querySelector('#stat2').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>No. users selected:</strong>&nbsp;${Number(total_unique_users).toLocaleString()}
        </div>`
        document.querySelector('#stat3').innerHTML = `
        <div class="d-flex justify-content-center ">
        <strong>No. posts scraped:</strong>&nbsp;${Number(total_scraped).toLocaleString()}
        </div>`
        document.querySelector('#stat4').innerHTML = `
        <div class="d-flex justify-content-center ">
            <strong>No. posts relevant:</strong>&nbsp;${Number(total_relevant).toLocaleString()}
        </div>`
}

