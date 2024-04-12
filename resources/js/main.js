

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

    const propertyList = document.querySelector('#property-list')

    if (propertyList) {

        const editProperty = (id) => {
            openModalProperty(id);
        }

        const deleteBtn = propertyList.querySelectorAll('[data-delete]'),
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
    }

    // edit building
    const buildHome = document.querySelector('#modal-building-edit')

    if (buildHome) {
        const list = document.querySelector('[data-list]'),
            btnEdit = list.querySelectorAll('[data-edit]'),
            btnDelete = list.querySelectorAll('[data-delete]'),
            btnCreate = document.querySelector('#modal-building-create')


        const saveClose = buildHome.querySelector('#modal-save'),
            closeBtn = buildHome.querySelector('#modal-close');

        const input1 = buildHome.querySelector('#id_kadasrt'),
            input2 = buildHome.querySelector('#buildingname'),
            input3 = buildHome.querySelector('#land'),
            input4 = buildHome.querySelector('#material'),
            input5 = buildHome.querySelector('#wear'),
            input6 = buildHome.querySelector('#flow'),
            input7 = buildHome.querySelector('#comment')

        const openModal = () => {
            buildHome.classList.remove('hidden')
        }

        closeBtn.addEventListener('click', () => closeModal())

        const deleteItem = async (id) => {
            axios.delete('/materil/building/delete',
                {
                    id_building: id
                }
            )
        }

        const form = buildHome.querySelector('#modal-building-form')

        buildHome.addEventListener('submit', async (e) => {
            e.preventDefault()

        })

        const closeModal = () => {
            input1.value = ""
            input2.value = ""
            input3.value = ""
            input4.value = ""
            input5.value = ""
            input6.value = ""
            input7.value = ""

            buildHome.classList.add('hidden')
        }

        const openModalEdit = async (id) => {

            const { data } = await axios.get(`/materil/building/edit/${id}`)

            input1.value = data.kadastr
            input2.value = data.buildingname
            input3.value = data.land
            input4.value = data.material
            input5.value = data.wear
            input6.value = data.flow
            input7.value = data.comment

            const submitDates = async () => {
                const res = await axios.patch(`/materil/building/edit`, {
                    buildingname: input2.value,
                    land: input3.value,
                    material: input4.value,
                    wear: input5.value,
                    flow: input6.value,
                    comment: input7.value,
                    id_kadastr: input1.value,
                    id_building: id
                })
                    .then(res => {
                        if (res.status == 200) {
                            saveClose.removeEventListener('click', async () => await submitDates())
                            window.location.reload()
                        }
                    }
                    )
            }

            saveClose.addEventListener('click', async () => await submitDates())

            openModal()
        }

        const openModalCreate = async () => {

            const sumbitCreater = async () => {
                data = {
                    id_kadastr: input1.value,
                    buildingname: input2.value,
                    land: input3.value,
                    material: input4.value,
                    wear: input5.value,
                    flow: input6.value,
                    comment: input7.value
                }

                await axios.post(`/materil/building/create`, {
                    ...data
                })
                    .then(res => {
                        if (res.status == 200) {
                            window.location.reload()
                        }
                    })
                    .catch(error => alert('Произошла ошибка!'))
            }

            buildHome.addEventListener('submit', async (e) => await sumbitCreater())

            openModal()
        }

        const deleteBuilding = async (id) => {
            await axios.delete(`/materil/building/delete`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    data: {
                        id_building: id
                    }
                })
                .then((res) => {
                    if (res.status == 200) {
                        window.location.reload()
                    }
                })
                .catch(
                    error => alert('Произошла ошибка!')
                )
        }

        btnCreate.addEventListener('click', async () => await openModalCreate())

        btnEdit.forEach(element => {
            element.addEventListener('click', async () => await openModalEdit(element.getAttribute('data-edit')))
        })

        btnDelete.forEach(element => {
            element.addEventListener('click', async () => await deleteBuilding(element.getAttribute('data-delete')))
        })
    }

    const kadastrModal = document.querySelector('#modal-kadastr')

    if (kadastrModal) {
        const list = document.querySelector('#kadastr-table'),
            form = kadastrModal.querySelector('#modal-kadastr-form')

        // btn
        const btnEdit = list.querySelectorAll('[data-edit]'),
            btnDelete = list.querySelectorAll('[data-delete]'),
            btnCreate = document.querySelector('#modal-kadastr-create'),
            btnSave = document.querySelector('#modal-kadastr-save'),
            btnClose = document.querySelector('#modal-kadastr-cancel')

        // inputs
        const input1 = kadastrModal.querySelector('#id_kadastr'),
            input2 = kadastrModal.querySelector('#street'),
            input3 = kadastrModal.querySelector('#house'),
            input4 = kadastrModal.querySelector('#year')

        const getKadastr = async (id) => {
            const { data } = await axios.get(`/materil/kadastr/edit/${id}`)

            input1.value = data.id
            input2.value = data.street
            input3.value = data.house
            input4.value = data.year
        }

        const editKadastr = async (id) => {
            const res = await axios.patch(`/materil/kadastr/edit`, {
                id_kadastr: input1.value,
                street: input2.value,
                house: input3.value,
                year: input4.value,
            })
                .then(res => {
                    if (res.status == 200) {
                        window.location.reload()
                    }
                })
                .catch(error => alert('Произошла ошибка!'))
        }

        const openModal = () => {
            kadastrModal.classList.remove('hidden')
        }

        const closeModal = () => {

            input1.value = ""
            input2.value = ""
            input3.value = ""
            input4.value = ""

            kadastrModal.classList.add('hidden')
        }

        const submitEdit = async (e, id) => {
            e.preventDefault()
            await editKadastr(id)
        }

        const modalEdit = async (id) => {
            await getKadastr(id)

            form.removeEventListener('submit', async (e) => await createKadastr(e))

            form.addEventListener('submit', async (e) => submitEdit(e, id))

            openModal()
        }

        const deleteKadastr = async (id) => {
            await axios.delete(`/materil/kadastr/delete/${id}`)
                .then((res) => {
                    if (res.status == 200) {
                        if (res.data != false) {
                            window.location.reload()
                        } else {
                            alert("Удалить не получится из-за целостности базы!")
                        }
                    }
                })
                .catch(
                    error => alert('Произошла ошибка!')
                )

        }

        const createKadastr = async (e) => {
            e.preventDefault()

            await axios.post(`/materil/kadastr/create`, {
                id_kadastr: input1.value,
                street: input2.value,
                house: input3.value,
                year: input4.value,
            })
                .then(res => {
                    if (res.status == 200) {
                        window.location.reload()
                    }
                })
                .catch(error => alert('Произошла ошибка!'))
        }

        const openModalCreate = async () => {

            form.removeEventListener('submit', async (e) => submitEdit(e))

            form.addEventListener('submit', async (e) => await createKadastr(e))

            openModal()
        }

        btnCreate.addEventListener('click', async () => await openModalCreate())

        btnClose.addEventListener('click', () => closeModal())

        btnEdit.forEach(element => {
            element.addEventListener('click', async () => await modalEdit(element.getAttribute('data-edit')))
        })

        btnDelete.forEach(element => {
            element.addEventListener('click', async () => await deleteKadastr(element.getAttribute('data-delete')))
        })
    }
})