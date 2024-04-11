

document.addEventListener('DOMContentLoaded', () => {

    axios.defaults.xsrfCookieName = 'XSRF-TOKEN';
    axios.defaults.xsrfHeaderName = 'X-XSRF-TOKEN';

    const LoginForm = document.querySelector('#login-form')

    // login
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
                    }

                    if (data.role == "Материально. отвественный") {
                        window.location.href = "/materil"
                    }
                })
        }

    }
    // is form login
    if (LoginForm) {
        LoginForm.addEventListener("submit", toLogin)
    }


    // delete property
    const deletelProperty = async (id) => {
        const res = await axios.delete('/materil/property/delete',
            {
                headers: {
                    'Content-Type': 'application/json',
                },
                data: {
                    unitid: id
                }
            }
        )
            .then(res => {
                if (res.status == 200) {
                    window.location.reload()
                }
            })
            .catch(error => alert('Произошла ошибка!'))

    }

    // edit property
    const editProperty = (id) => {
        openModalProperty(id);
    }

    const propertyList = document.querySelector('#property-list'),
        deleteBtn = propertyList.querySelectorAll('[data-delete]'),
        editBtn = propertyList.querySelectorAll('[data-edit]');

    deleteBtn.forEach(element => {
        element.addEventListener('click', async () => await deletelProperty(element.getAttribute('data-delete')))
    });

    editBtn.forEach(element => {
        element.addEventListener('click', async () => editProperty(element.getAttribute('data-edit')))

    })

    const getPropertyOne = async (id) => {
        const { data } = await axios.get(`/materil/property/get/${id}`)
            .catch(error => alert('Произошла ошибка!'))

        return data
    }
    const modal = document.querySelector('#modal-property-edit'),
        close = document.querySelector('#modal-close')
    // Добавляем новый обработчик события
    close.addEventListener('click', closeModalHandler);

    // Определяем функцию обработчика для закрытия модального окна
    function closeModalHandler() {
        modal.classList.toggle('hidden');
    }

    const openModalProperty = async (id) => {
        const form = modal.querySelector('#property-form'),
            save = modal.querySelector('#modal-save')

        const input1 = form.querySelector('#unitname'),
            input2 = form.querySelector('#datestart'),
            input3 = form.querySelector('#cost'),
            input4 = form.querySelector('#costyear'),
            input5 = form.querySelector('#costafter'),
            input6 = form.querySelector('#period'),
            input7 = form.querySelector('#hallid')


        modal.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                unitid: id,
                unitname: input1.value,
                datestart: input2.value,
                cost: parseFloat(input3.value),
                costyear: Number(input4.value),
                costafter: Number(input5.value),
                period: Number(input6.value),
                hallid: Number(input7.value)
            }

            await axios.patch(`/materil/property/edit`, {
                ...data
            })
                .then(res => {
                    if (res.status == 200) {
                        window.location.reload()
                    }
                })
                .catch(error => alert('Произошла ошибка!'))
        })



        const data = await getPropertyOne(id)

        form.querySelector('#unitname').value = data[1]
        form.querySelector('#datestart').value = data[2]
        form.querySelector('#cost').value = data[3]
        form.querySelector('#costyear').value = data[4]
        form.querySelector('#costafter').value = data[5]
        form.querySelector('#period').value = data[6]
        form.querySelector('#hallid').value = data[7]

        modal.classList.toggle('hidden')

    }

    const openModalPropertyCreate = async () => {
        const form = modal.querySelector('#property-form'),
            save = modal.querySelector('#modal-save')

        const input1 = form.querySelector('#unitname'),
            input2 = form.querySelector('#datestart'),
            input3 = form.querySelector('#cost'),
            input4 = form.querySelector('#costyear'),
            input5 = form.querySelector('#costafter'),
            input6 = form.querySelector('#period'),
            input7 = form.querySelector('#hallid')


        input1.value = ""
        input2.value = ""
        input3.value = ""
        input4.value = ""
        input5.value = ""
        input6.value = ""
        input7.value = ""

        modal.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                unitname: input1.value,
                datestart: input2.value,
                cost: parseFloat(input3.value),
                costyear: Number(input4.value),
                costafter: Number(input5.value),
                period: Number(input6.value),
                hallid: Number(input7.value)
            }

            await axios.post(`/materil/property/create`, {
                ...data
            })
                .then(res => {
                    if (res.status == 200) {
                        window.location.reload()
                    }
                })
                .catch(error => alert('Произошла ошибка!'))
        })

        modal.classList.toggle('hidden')

    }

    document.querySelector('#create-property').addEventListener('click', async () => openModalPropertyCreate())
})