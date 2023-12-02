var tg = window.Telegram.WebApp;

// Расширяем на весь экран.
tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';
tg.MainButton.setText("Войти");
tg.MainButton.show();

let passwordInput = document.getElementById("password");
let submitBtn = document.getElementById("submitBtn");

submitBtn.addEventListener("click", function(e) {
	e.preventDefault();
	tg.MainButton.setText("Войти");
    tg.MainButton.show();
});


Telegram.WebApp.onEvent("mainButtonClicked", function(){
	if (passwordInput.value) {
		tg.sendData(passwordInput.value);
		passwordInput.value = '';
	}
});

let user_card = document.getElementById("user_card");
let p = document.createElement("p");
p.innerText = `${tg.initDataUnsafe.user.first_name}
${tg.initDataUnsafe.user.last_name}`;
user_card.appendChild(p);
