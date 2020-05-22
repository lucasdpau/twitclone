console.log("Hi!")

var ajaxFunction = function() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		ajaxTestButton.innerHTML = this.responseText;
		}
	};
	xhttp.open("GET", "/follow/q", true);
	xhttp.send();
};

ajaxTestButton = document.getElementById("jstest");
ajaxTestButton.onclick = ajaxFunction;




var likeTweet = function() {

}

var likeButtons = document.querySelectorAll(".like_button");
for (var i=0; i<likeButtons.length; i++) {
	likeButtons[i].onclick = function(){}
}


var unlikeButtons = document.querySelectorAll(".unlike_button");
for (var i=0; i<unlikeButtons.length; i++) {
	unlikeButtons[i].onclick = function(){}
}