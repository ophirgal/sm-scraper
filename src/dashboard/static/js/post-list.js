function renderPostList() {
    var sampleText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in magna nisl. Nunc convallis et risus id varius. Aliquam elit quam, hendrerit nec urna sit amet, iaculis pulvinar elit. Phasellus vel pharetra orci. Sed vel ante consequat nisl commodo scelerisque. Suspendisse feugiat magna ac metus aliquet rutrum.";

    if (postList.length == 0) { // for testing without data!
      postList = [{'title': 'Post 1', 'body': sampleText},{'title': 'Post 2', 'body': sampleText},{'title': 'Post 3', 'body': sampleText}];
    }
    var listNode = document.getElementById("postlist");
    clearNode(listNode);
    // build list item and append for each post
    postList.forEach(post => {
      var node = document.createElement("div"); 
      node.classList.add("mb-2", "p-2", "rounded", "shadow-1-strong", "bg-white");

      var titleNode = document.createElement("div");
      titleNode.classList.add("mb-1");
      var textNode = document.createTextNode(post.title);
      titleNode.appendChild(textNode);  
      node.appendChild(titleNode);

      var titleNode = document.createElement("div");
      var textNode = document.createTextNode(post.body);
      titleNode.appendChild(textNode);  
      node.appendChild(titleNode);

      listNode.appendChild(node);
    });
}