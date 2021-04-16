function addSources(e) {
    var list = e.target.value.trim().split(" ");
    e.target.value = "";
    sources = sources.concat(list).unique().noSpace();
    updateSourcePills();
}

function removeSource(s) {
    sources = sources.filter(e => e !== s);
    updateSourcePills();
}

function updateSourcePills() {
    var pillListNode = document.getElementById("source-pill-list");
    clearNode(pillListNode);
    pillListNode.appendChild(buildPillList(sources, "bg-orange", removeSource));
}