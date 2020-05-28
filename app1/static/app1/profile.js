var likeTweet = function(tweet_like_button, like_unlike) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		if (this.responseText == "NotLoggedIn") {
			window.location.href = "/login";
		}
		else {
			tweet_like_button.innerHTML = this.responseText;
			tweet_like_button.setAttribute("value", this.responseText.toLowerCase());
			}
		}
	};
	xhttp.open("POST", "/like/" + tweet_like_button.tweet_id, true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("likeunlike=" + like_unlike);
}


var followProfile = function(followButton) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		if (this.responseText == "NotLoggedIn") {
			window.location.href = "/login";
		}
		else {
			followButton.innerHTML = this.responseText;
			followButton.setAttribute("value", this.responseText.toLowerCase());
			}	
		}
	};
	xhttp.open("POST", "/follow/" + followButton.getAttribute('name').substr(12), true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send();
}


var likeButtons = document.querySelectorAll(".like_button");
for (var i=0; i<likeButtons.length; i++) {
// each button has an id of 'likebutton<tweet_id>', so we slice out the first 10 chars to isolate <tweet_id>
	(function(index) {
		likeButtons[index].tweet_id = likeButtons[index].getAttribute("id").substr(10);
		likeButtons[index].addEventListener("click", function() {
			likeTweet(likeButtons[index], likeButtons[index].getAttribute("value"));
		})
	})(i);
}


var followButton = document.getElementById("followButton");
if (followButton) {
	followButton.addEventListener("click", function() {
		followProfile(followButton);
	})
}