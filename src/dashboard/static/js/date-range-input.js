/* Date range pickers and period buttons */

function dateRangeSelect(val) {
    dateRangeSetting = val;
    updateDateRange();
}

function updateDateRange() {
    updateDateRangePickers();
    updateDateRangeButtons();
}

function updateDateRangePickers() { 
    if (dateRangeSetting != "Custom") {
        var startNode = document.getElementById("start");
        var endNode = document.getElementById("end");

        var startDate = new Date();
        var endDate = new Date();
        var diff = 0;
        switch (dateRangeSetting) {
            case "1D":
                diff = 1;
                break;
            case "1W":
                diff = 7;
                break;
            case "1M":
                diff = 31;
                break;
            case "3M":
                diff = 91;
                break;
            case "1Y":
                diff = 365;
                break;
            case "All":
                diff = 10000;
                break;
        }
        startDate.setDate(startDate.getDate()-diff);
        startNode.value = startDate.toISOString().split('T')[0];
        endNode.value = endDate.toISOString().split('T')[0];
    }
    
}

function updateDateRangeButtons() {
    toggleDateButton("1D-button", false);
    toggleDateButton("1W-button", false);
    toggleDateButton("1M-button", false);
    toggleDateButton("3M-button", false);
    toggleDateButton("1Y-button", false);
    toggleDateButton("All-button", false);
    switch (dateRangeSetting) {
        case "1D":
            toggleDateButton("1D-button", true);
            break;
        case "1W":
            toggleDateButton("1W-button", true);
            break;
        case "1M":
            toggleDateButton("1M-button", true);
            break;
        case "3M":
            toggleDateButton("3M-button", true);
            break;
        case "1Y":
            toggleDateButton("1Y-button", true);
            break;
        case "All":
            toggleDateButton("All-button", true);
            break;
        // Custom range case, do nothing
    }
}

function toggleDateButton(id, val) {
    var node = document.getElementById(id);
    if (val) {
        node.classList.remove("btn-light");
        node.classList.add("btn-primary");
    }
    else {
        node.classList.remove("btn-primary");
        node.classList.add("btn-light");
    }
    //node.disabled = val;
}