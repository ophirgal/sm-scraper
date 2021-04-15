function dateRangeSelect(val) {
    dateRangeSetting = val;
    updateDateRangeButtons();
}

function updateDateRangeButtons() {
    var button1D = document.getElementById("1D-button");
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