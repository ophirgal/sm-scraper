function buildPillList(stringList, color, removeFunc) {
    var pillListNode = document.createElement("div"); 
    stringList.forEach(word => {
        var node = document.createElement("div"); 
        node.classList.add("pill", "mb-1", "p-1", "rounded", color, "text-white");
        node.onclick = function() { removeFunc(word); }

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