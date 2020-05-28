var likeTweet = function(tweet_like_button, like_unlike) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		tweet_like_button.innerHTML = this.responseText;
		tweet_like_button.setAttribute("value", this.responseText.toLowerCase());
		}
	};
	xhttp.open("POST", "/like/" + tweet_like_button.tweet_id, true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("likeunlike=" + like_unlike);
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