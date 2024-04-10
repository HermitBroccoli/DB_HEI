

document.addEventListener('DOMContentLoaded', () => {

    axios.defaults.xsrfCookieName = 'XSRF-TOKEN';
    axios.defaults.xsrfHeaderName = 'X-XSRF-TOKEN';

    const LoginForm = document.querySelector('#login-form')

    const toLogin = async (e) => {
        e.preventDefault()
        const login = LoginForm.querySelector('#login'),
            password = LoginForm.querySelector('#password')

        if (login.value != "" && password.value != "") {
            const response = await axios.post('/login', {
                login: login.value,
                password: password.value
            })
            .then(res => {
                const { data } = res

                if (data.role == "Администратор") {
                    window.location.href = "/admin"
                } else if (data.role == "Материально. отвественный") {}
                else {}
            })
    }

    }

    if (LoginForm) {
        LoginForm.addEventListener("submit", toLogin)
    }
})