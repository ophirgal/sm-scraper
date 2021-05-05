function addSources(e) {
    //var list = e.target.value.trim().split(" ");
    var source = e.target.value.trim();
    e.target.value = "";
    //sources = sources.concat(list).unique().noSpace();
    sources.push(source);
    sources = sources.unique().noSpace();
    updateSourcePills();
    renderAll();
}

function removeSource(s) {
    sources = sources.filter(e => e !== s);
    updateSourcePills();
    renderAll();
}

function updateSourcePills() {
    var pillListNode = document.getElementById("source-pill-list");
    clearNode(pillListNode);
    pillListNode.appendChild(buildPillList(sources, "bg-orange", removeSource));
}