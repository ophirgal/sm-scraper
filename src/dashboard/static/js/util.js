
// clears existing list items
function clearNode(node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
}

// removes duplicates from array of strings
Array.prototype.unique = function() {
    var a = this.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j--, 1);
        }
    }
    return a;
};

// removes spaces or empty string from array of strings
Array.prototype.noSpace = function() {
    var a = this.concat();
    var n = [];
    for(var i=0; i<a.length; ++i) {
        if (a[i] != " " && a[i] != "") {
            n.push(a[i]);
        }
    }
    return n;
};