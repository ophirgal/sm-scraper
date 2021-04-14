function addJurisdictions(e) {
    var list = e.target.value.trim().split(" ");
    e.target.value = "";
    jurisdictions = jurisdictions.concat(list).unique().noSpace();
    updateJurisdictionPills();
}

function removeJurisdiction(s) {
    jurisdictions = jurisdictions.filter(e => e !== s);
    updateJurisdictionPills();
}

function updateJurisdictionPills() {
    var pillListNode = document.getElementById("jurisdiction-pill-list");
    clearNode(pillListNode);
    pillListNode.appendChild(buildPillList(jurisdictions, "bg-primary"));
}