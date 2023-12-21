const nav = document.getElementById('nav');

function handleLogout() {
    fetch('/auth/logout', {
        method: 'POST',
    })
        .then((response) => {
            if (response.status === 204) {
                location.href = "/pages/login";
            } else if (response.status === 401) {
                showModal('Вы не авторизованы.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function handleRecords() {
    location.href = '/pages/records';
}

function handleLogin() {
    location.href = '/pages/login';
}

function handleRegister() {
    location.href = '/pages/register';
}

fetch('/users/me')
    .then(response => {
        if (response.status === 200) {
            nav.innerHTML = '<button id="logoutBtn">Выйти</button><button id="recordsBtn">Мои пароли</button>';
            document.getElementById('logoutBtn').addEventListener('click', handleLogout);
            document.getElementById('recordsBtn').addEventListener('click', handleRecords);
        } else if (response.status === 401) {
            nav.innerHTML = '<button id="loginBtn">Авторизация</button><button id="registerBtn">Регистрация</button>';
            document.getElementById('loginBtn').addEventListener('click', handleLogin);
            document.getElementById('registerBtn').addEventListener('click', handleRegister);
        }
    })
    .catch(error => console.error('Error:', error));
