function addKeywords(e) {
    var list = e.target.value.trim().split(" ");
    e.target.value = "";
    keywords = keywords.concat(list).unique();
    updateKeywordPills();
}

function removeKeyword(s) {
    keywords = keywords.filter(e => e !== s);
    updateKeywordPills();
}

function updateKeywordPills() {
    var pillListNode = document.getElementById("keyword-pill-list");
    clearNode(pillListNode);
    keywords.forEach(word => {
        var node = document.createElement("div"); 
        node.classList.add("pill", "mb-1", "p-1", "rounded", "bg-primary", "text-white");
        node.onclick = function() { removeKeyword(word); }

        var textNode = document.createTextNode(word);
        node.appendChild(textNode);  

        pillListNode.appendChild(node);
    });
}