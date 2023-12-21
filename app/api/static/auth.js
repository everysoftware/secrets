const passwordInput = document.getElementById('password');
const togglePasswordCheckbox = document.getElementById('togglePassword');

togglePasswordCheckbox.addEventListener('click', function () {
    if (togglePasswordCheckbox.checked) {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Предотвращает перезагрузку страницы

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const formData = new URLSearchParams();
    formData.append('grant_type', 'password');
    formData.append('username', username);
    formData.append('password', password);

    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    })
        .then((response) => {
            if (response.status === 204) {
                window.location.href = "/pages/records";
            } else if (response.status === 400) {
                showModal('Неверный логин или пароль.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
})

function showModal(message) {
    let mainContent = document.getElementById('content')

    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.right = '0';
    modal.style.bottom = '0';
    modal.style.left = '0';
    modal.style.background = 'rgba(0, 0, 0, 0.5)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.padding = '50px';
    modal.style.boxSizing = 'border-box';
    modal.style.zIndex = '1000';
    mainContent.appendChild(modal);

    const modalContent = document.createElement('div');
    modalContent.style.background = '#fff';
    modalContent.style.padding = '20px';
    modalContent.style.borderRadius = '10px';
    modalContent.style.maxWidth = '100%';
    modalContent.style.boxSizing = 'border-box';

    const text = document.createElement('p');
    text.textContent = message;
    modalContent.appendChild(text);

    const closeButton = document.createElement('button');
    closeButton.textContent = 'Закрыть';
    closeButton.style.padding = '10px 20px'; // Увеличиваем размер кнопки
    closeButton.style.border = 'none'; // Убираем рамку
    closeButton.style.borderRadius = '5px'; // Добавляем скругление углов
    closeButton.style.background = '#ff6347'; // Изменяем цвет фона
    closeButton.style.color = '#fff'; // Изменяем цвет текста
    closeButton.style.cursor = 'pointer'; // Добавляем эффект наведения
    closeButton.addEventListener('click', function () {
        document.body.removeChild(modal);
    });
    modalContent.appendChild(closeButton);

    modal.appendChild(modalContent);
    document.body.appendChild(modal);
}
