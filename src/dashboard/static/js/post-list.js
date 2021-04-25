async function renderPostList() {
    // fetch stats data from server
    let url = new URL("http://localhost:5000/get-posts"),
        params = {
            p1: 35.696233,
            p2: 139.570431
        }
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    let posts = await fetch(url, { "credentials": "same-origin" })
        .then(response => response.json())

    postList = posts.postList;
    for (var i = 0; i < postList.length; i++) {
      post = postList[i];
      if (post.body.length > 400) {
        post.body = post.body.substring(0,400) + " ...";
      }
      postList[i] = post;
    }

    /////////////////// FOR TESTING WHEN NO DATA
    if (postList.length == 0) { // for testing without data!
      var sampleText = "Lorem ipsum dolor sit amet, convallis et risus id varius. Aliquam elit quam, hendrerit nec urna sit amet, iaculis pulvinar elit. Phasellus vel pharetra orci. Sed vel ante consequat nisl commodo scelerisque. Suspendisse feugiat magna ac metus aliquet rutrum.";
      postList = [
        {
          'relevance_score': "1",
          'platform': "Reddit",
          'subplatform': "PoliceBrutality",
          'time_posted': "2021-04-01",
          'time_scraped': "2021-04-02",
          'title': 'Post 1 Title', 
          'body': sampleText, 
          'author': "JohnSmith", 
          'post_url': "https://google.com",
          'linked_urls': "https://google.com",
          'comment_count': "100",
          'rating': "1200"
        },
        {
          'relevance_score': "2",
          'platform': "Reddit",
          'subplatform': "Justice",
          'time_posted': "2021-03-01",
          'time_scraped': "2021-04-03",
          'title': 'Post 2 Title', 
          'body': sampleText, 
          'author': "JohnSmith", 
          'post_url': "https://google.com",
          'linked_urls': "",
          'comment_count': "5",
          'rating': "25"
        },
        {
          'relevance_score': "3",
          'platform': "Reddit",
          'subplatform': "PoliceBrutality",
          'time_posted': "2021-03-05",
          'time_scraped': "2021-04-03",
          'title': 'Post 3 Title', 
          'body': sampleText, 
          'author': "JohnSmith", 
          'post_url': "https://google.com",
          'linked_urls': "",
          'comment_count': "500",
          'rating': "4234"
        },
        {
          'relevance_score': "4",
          'platform': "Reddit",
          'subplatform': "Police",
          'time_posted': "2021-04-02",
          'time_scraped': "2021-04-03",
          'title': 'Post 4 Title', 
          'body': sampleText, 
          'author': "JohnSmith", 
          'post_url': "https://google.com",
          'linked_urls': "",
          'comment_count': "50",
          'rating': "20"
        }
      ];
    }
    
    // sorting
    var sortMetric = document.getElementById("sort-posts-metric").value;
    var sortedPostList = sortPosts(postList, sortMetric);

    var listNode = document.getElementById("postlist");
    clearNode(listNode);
    
    // build list item and append for each post
    sortedPostList.forEach(post => {
      listNode.appendChild(buildPostCard(post));
    });
}

function sortPosts(postList, sortMetric) {
  switch (sortMetric) {
    case "relevance":
      postList.sort((p1, p2) => {
        var v1 = parseInt(p1.relevance_score);
        var v2 = parseInt(p2.relevance_score);
        if (v1 > v2) return -1;
        if (v1 < v2) return 1;
        return 0;
      });
      break;
    case "date":
      postList.sort((p1, p2) => {
        var v1 = Date.parse(p1.time_posted);
        var v2 = Date.parse(p2.time_posted);
        if (v1 > v2) return -1;
        if (v1 < v2) return 1;
        return 0;
      });
      break;
    case "rating":
      postList.sort((p1, p2) => {
        var v1 = parseInt(p1.rating);
        var v2 = parseInt(p2.rating);
        if (v1 > v2) return -1;
        if (v1 < v2) return 1;
        return 0;
      });
      break;
    case "comments":
      postList.sort((p1, p2) => {
        var v1 = parseInt(p1.comment_count);
        var v2 = parseInt(p2.comment_count);
        if (v1 > v2) return -1;
        if (v1 < v2) return 1;
        return 0;
      });
      break;
  }

  return postList;
}

function buildPostCard(post) {
  var node = document.createElement("div"); 
  node.classList.add("mb-2", "p-2", "rounded", "shadow-1-strong", "bg-white");

  node.appendChild(buildInfoRow(post));
  node.appendChild(buildTitle(post));
  node.appendChild(buildContentLink(post));
  node.appendChild(buildBody(post));
  node.appendChild(buildStats(post));

  return node;
}

function join(t, a, s) {
  function format(m) {
     let f = new Intl.DateTimeFormat('en', m);
     return f.format(t);
  }
  return a.map(format).join(s);
}

function buildInfoRow(post) {
  // subreddit
  var infoRow = document.createElement("div");
  infoRow.classList.add("mb-0", "font-medium", "font-bold");

  var redditPrefix = post.platform == "Reddit" ? "r/" : "";
  var subReddit = document.createElement('a');
  var subText = document.createTextNode(redditPrefix + post.subplatform);
  subReddit.appendChild(subText);  
  subReddit.href = "https://www.reddit.com/r/" + post.subplatform;
  infoRow.appendChild(subReddit);  

  var textNode = document.createTextNode(" • Posted by ");
  infoRow.appendChild(textNode);  

  var userPrefix = post.platform == "Reddit" ? "u/" : "";
  var user = document.createElement('a');
  var userText = document.createTextNode(userPrefix + post.author);
  user.appendChild(userText);  
  user.href = "https://www.reddit.com/user/" + post.author;
  infoRow.appendChild(user);  

  let a = [{day: 'numeric'}, {month: 'short'}, {year: 'numeric'}];
  var textNode = document.createTextNode(
    " on " + join(Date.parse(post.time_posted), a, ' ') 
    + " • Last updated on " + join(Date.parse(post.time_scraped), a, ' '));
  infoRow.appendChild(textNode);  
  return infoRow;
}

function buildTitle(post) { 
  var titleContainer = document.createElement("div");
  titleContainer.classList.add("font-large");
  var a = document.createElement('a');
  var textNode = document.createTextNode(post.title);
  a.appendChild(textNode);  
  a.href = post.post_url;
  titleContainer.appendChild(a);  
  return titleContainer;
}


function buildContentLink(post) { 
  var contentLinkContainer = document.createElement("div");
  if (post.linked_urls.length == 0) return contentLinkContainer; 
  contentLinkContainer.classList.add("mb-1", "font-small");
  var a = document.createElement('a');
  var textNode = document.createTextNode(post.linked_urls);
  a.appendChild(textNode);  
  a.href = post.post_url;
  contentLinkContainer.appendChild(a);  
  return contentLinkContainer;
}

function buildBody(post) { 
  var bodyContainer = document.createElement("div");
  bodyContainer.classList.add("mb-1", "font-medium");
  var textNode = document.createTextNode(post.body);
  bodyContainer.appendChild(textNode);  
  return bodyContainer;

}

function buildStats(post) { 
  var statsContainer = document.createElement("div");
  statsContainer.classList.add("mb-1", "font-medium");
  var textNode = document.createTextNode(post.rating + "▲ • " + post.comment_count + " comments");
  statsContainer.appendChild(textNode);  
  return statsContainer;
}
