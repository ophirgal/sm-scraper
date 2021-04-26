
// clears existing list items
function clearNode(node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
}

// date formatting
function join(t, a, s) {
    function format(m) {
       let f = new Intl.DateTimeFormat('en', m);
       return f.format(t);
    }
    return a.map(format).join(s);
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

// handler for vis button clicks ('Select' vs. 'All')
function visBtnClicked(e) { 
    e.target.classList.remove("btn-gray")
    e.target.classList.add("btn-primary") 
    let otherBtn = document.getElementById(e.target.getAttribute('other_id'))
    otherBtn.classList.remove("btn-primary")
    otherBtn.classList.add("btn-gray")
    renderAll(false, true, true, false)
}
