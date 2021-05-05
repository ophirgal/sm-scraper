function addJurisdictions(e) {
    var jur = e.target.value.trim();
    e.target.value = "";
    //jurisdictions = jurisdictions.concat(list).unique().noSpace();
    jurisdictions.push(jur);
    jurisdictions = jurisdictions.unique().noSpace();
    updateJurisdictionPills();
    renderAll();
}

function removeJurisdiction(s) {
    jurisdictions = jurisdictions.filter(e => e !== s);
    updateJurisdictionPills();
    renderAll();
}

function updateJurisdictionPills() {
    var pillListNode = document.getElementById("jurisdiction-pill-list");
    clearNode(pillListNode);
    pillListNode.appendChild(buildPillList(jurisdictions, "bg-primary", removeJurisdiction));
}