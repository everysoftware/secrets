document.addEventListener("DOMContentLoaded", function() {
    var tg = window.Telegram.WebApp;

    tg.MainButton.textColor = '#FFFFFF';
    tg.MainButton.color = '#52BE80';
    tg.MainButton.setText("Войти");
    tg.MainButton.disable();
    tg.MainButton.show();

    let passwordInput = document.getElementById("password");

    passwordInput.addEventListener("input", function(e) {
        e.preventDefault();
        if (passwordInput.value) {
            tg.MainButton.color = '#2cab37';
            tg.MainButton.enable();
        } else {
            tg.MainButton.color = '#52BE80';
            tg.MainButton.disable();
        }
    });

    Telegram.WebApp.onEvent("mainButtonClicked", function(){
        if (passwordInput.value) {
            tg.sendData(passwordInput.value);
            passwordInput.value = '';
        }
    });
});
