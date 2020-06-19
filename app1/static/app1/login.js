const forgotPasswordDiv = document.getElementById("login_forgot_password");
forgotPasswordDiv.addEventListener('click', function(){
	forgotPasswordDiv.innerHTML = "Log in with username: test, password: test";
	forgotPasswordDiv.style.color = "black";
	forgotPasswordDiv.style["text-decoration"] = "none";
	forgotPasswordDiv.style.cursor = "auto";
});