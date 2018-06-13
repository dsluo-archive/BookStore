window.onload = function() {
	console.log("I AM READING THE SCRIPT");
	var popup = document.getElementById('myPopup');
	var doLogin = document.getElementById("doLogin");
	
	doLogin.onclick = function() {
        "use strict";
        clearValues();
        currentSubmit = "#login";
        popup.style.display = "block";
	};
}