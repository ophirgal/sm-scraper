function buildPillList(stringList) {
    var pillListNode = document.createElement("div"); 
    stringList.forEach(word => {
        var node = document.createElement("div"); 
        node.classList.add("pill", "mb-1", "p-1", "rounded", "bg-primary", "text-white");
        node.onclick = function() { removeKeyword(word); }

        var textContainer = document.createElement("div"); 
        textContainer.classList.add("pr-2", "inline");
        var textNode = document.createTextNode(word);
        textContainer.appendChild(textNode);
        node.appendChild(textContainer);  

        var xContainer = document.createElement("div");
        xContainer.classList.add("pr-1", "inline");
        var xImg = document.createElement('img');
        xImg.style.height = "12px";
        xImg.style.width = "12px";
        xImg.src = "./static/img/transparent-x.png";
        xContainer.appendChild(xImg);
        node.appendChild(xContainer);

        pillListNode.appendChild(node);
    });
    return pillListNode
}