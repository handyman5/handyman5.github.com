let BLUESKY_DID;
let BLUESKY_POST_ID;

function embedPost(parentId, uri) {
  const parent = document.getElementById(parentId);
  const corsproxy_uri =
    "https://corsproxy.io?" +
    encodeURIComponent(`https://embed.bsky.app/oembed?url=${uri}`);

  let commentId = Math.random().toString();
  content = document.createElement("div");
  content.setAttribute("id", commentId);
  parent.appendChild(content);

  fetch(corsproxy_uri, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then(function (response) {
      console.log(response.status);
      if (response.status == 200) {
        return response.json();
      }
    })
    .then(function (data) {
      if (typeof data !== "undefined") {
        elem = document.getElementById(commentId);
        elem.innerHTML = data.html;

        embed = document.createElement("script");
        embed.src = "https://embed.bsky.app/static/embed.js";
        parent.appendChild(embed);
      }
    });
}

function loadComments() {
  const commentsWrapper = document.getElementById("comments-wrapper");

  if (BLUESKY_POST_ID.includes("https:")) {
    BLUESKY_POST_ID = BLUESKY_POST_ID.split("/").pop();
  }

  // example
  // uri = 'at://did:plc:ekcyikfp2mpymgtyzz7wkfuj/app.bsky.feed.post/3lbzgeshvqs2p'

  // mine
  // uri = 'at://did:plc:yxhvd47p53gmb5zfiktqq3og/app.bsky.feed.post/3kvakhzcwjc2k'

  // mine with one comment
  // uri = 'at://did:plc:yxhvd47p53gmb5zfiktqq3og/app.bsky.feed.post/3kvyb6maweh2w'

  // mine with no comments
  // uri = 'at://did:plc:yxhvd47p53gmb5zfiktqq3og/app.bsky.feed.post/3lc5amtplcc2i'

  // dynamic uri
  uri = `at://${BLUESKY_DID}/app.bsky.feed.post/${BLUESKY_POST_ID}`;

  try {
    console.log("Starting fetch for comments at:", new Date().toLocaleString());
    const endpoint = `https://api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=${encodeURIComponent(uri)}`;
    console.log("Endpoint:", endpoint);

    const response = fetch(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    })
      .then(function (response) {
        try {
          return response.json();
        } catch (e) {
          error = e.message;
          console.error("Error with embedPost fetching comments:", e);
        }
      })
      .then(function (data) {
        embedPost("comments-wrapper", data.thread.post.uri);

        const replies = data.thread.replies;
        if (replies && Array.isArray(replies) && replies.length > 0) {
          replies.forEach(function (item) {
            embedPost("comments-wrapper", item.post.uri);
          });
        }
      });
  } catch (e) {
    error = e.message;
    console.error("Error fetching comments:", e);
  }
}
// hoodley-hoo
