var tg = window.Telegram.WebApp;

// Расширяем на весь экран.
tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

let passwordInput = document.getElementById("password");
let submitBtn = document.getElementById("submitBtn");

submitBtn.addEventListener("click", function(e) {
	e.preventDefault();
	tg.MainButton.show();
});


Telegram.WebApp.onEvent("mainButtonClicked", function(){
	if (passwordInput.value) {
		tg.sendData(passwordInput.value);
		passwordInput.value = '';
	}
});
