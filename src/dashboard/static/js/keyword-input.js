function addKeywords(e) {
    var list = e.target.value.trim().split(" ");
    e.target.value = "";
    keywords = keywords.concat(list).unique().noSpace();
    updateKeywordPills();
    renderAll();
}

function removeKeyword(s) {
    keywords = keywords.filter(e => e !== s);
    updateKeywordPills();
    renderAll();
}

function updateKeywordPills() {
    var pillListNode = document.getElementById("keyword-pill-list");
    clearNode(pillListNode);
    pillListNode.appendChild(buildPillList(keywords, "bg-success", removeKeyword));
}
