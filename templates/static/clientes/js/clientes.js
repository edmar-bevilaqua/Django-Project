//const { header } = require("express/lib/request")

function add_pet(){
    container = document.getElementById('form-pet')
    html = "<div class='row pet'>\
                    <div class='col-md-4'>\
                        <label for='pet'>Pet Name:</label>\
                        <input type='text' placeholder='Pet Name' class='form-control' name='pet'>\
                    </div>\
                    <div class='col-md-4'>\
                        <label for='data-nascimento'>Birth Date:</label>\
                        <input type='date' placeholder='DD/MM/YYYY' class='form-control' name='data-nascimento'>\
                    </div>\
                    <div class='col-md-3'>\
                        <label for='porte'>Pet Size:</label>\
                        <select name='porte' class='form-control'>\
                            <option value='pequeno'>Small</option>\
                            <option value='medio'>Medium</option>\
                            <option value='grande'>Big</option>\
                        </select>\
                    </div>\
                    <div class='col-md-1 delete'>\
                        <button onclick='deleteRow(this)' class='btn btn-danger'><i class='bi bi-trash3-fill'></i></button>\
                    </div>\
                </div>"

    container.innerHTML += html
}

function add_pet_atualiza(){
    cliente = document.getElementById("cliente-select").value
    container = document.getElementById('add-pets')
    html = "<br><form action='/clientes/add-pet/" + cliente + "' method='POST'>\
                    <div class='row'>\
                        <div class='col-md-4'>\
                            <label for='pet'>Pet Name:</label>\
                            <input type='text' placeholder='Pet Name' class='form-control' name='pet'>\
                        </div>\
                        <div class='col-md-3'>\
                            <label for='data-nascimento'>Birth Date:</label>\
                            <input type='date' placeholder='DD/MM/YYYY' class='form-control' name='data-nascimento'>\
                        </div>\
                        <div class='col-md-3'>\
                            <label for='porte'>Pet Size:</label>\
                            <select name='porte' class='form-control'>\
                                <option value='pequeno'>Small</option>\
                                <option value='médio'>Medium</option>\
                                <option value='grande'>Big</option>\
                            </select>\
                        </div>\
                        <div class='col-md-2 btn-register'>\
                            <input class='btn btn-success add' type='submit' value='Add'>\
                        </div>\
                    </div>\
                </form>"
    container.innerHTML += html
}

function exibir_form(type) {
    add_cliente = document.getElementById("adicionar-cliente")
    att_cliente = document.getElementById("atualizar-cliente")

    if(type == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"
    } else if(type == "2"){
        att_cliente.style.display = "block"
        add_cliente.style.display = "none"
    }
}

function dados_cliente() {
    cliente = document.getElementById("cliente-select")
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch('/clientes/atualizar_cliente', {
        method:'POST',
        headers:{'X-CSRFToken' : csrf_token},
        body: data
    }).then(response => response.json()).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'
        document.getElementById('opt-add-pets').style.display = 'block'
        document.getElementById('add-pets').innerHTML = ""

        id = document.getElementById('id')
        id.value = data['cliente_id']

        att_nome = document.getElementById('att-nome')
        att_nome.value = data['clientes']['nome']

        att_sobrenome = document.getElementById('att-sobrenome')
        att_sobrenome.value = data['clientes']['sobrenome']

        att_email = document.getElementById('att-email')
        att_email.value = data['clientes']['email']

        att_cpf = document.getElementById('att-cpf')
        att_cpf.value = data['clientes']['cpf']

        div_pets = document.getElementById('lista-pets')

        div_pets.innerHTML = ""
        console.log(data)

        for(i=0; i<data['pets'].length; i++){
            
            div_pets.innerHTML += "<form action='/clientes/atualiza-pet/" + data['pets'][i]['id'] + "' method='POST'>\
                                        <div class='row'>\
                                            <div class='col-md-4'>\
                                                <label for='pet'>Pet Name:</label>\
                                                <input type='text' placeholder='Pet Name' class='form-control' name='pet' value='" + data['pets'][i]['fields']['nome_pet'] + "'>\
                                            </div>\
                                            <div class='col-md-3'>\
                                                <label for='data-nascimento'>Birth Date:</label>\
                                                <input type='date' placeholder='DD/MM/YYYY' class='form-control' name='data-nascimento' value='" + data['pets'][i]['fields']['data_nascimento_pet'] + "'>\
                                            </div>\
                                            <div class='col-md-3'>\
                                                <label for='porte'>Pet Size:</label>\
                                                <select name='porte' class='form-control'>\
                                                    <option value='" + data['pets'][i]['fields']['porte'] + "' selected hidden>" + data['pets'][i]['fields']['porte'] + "</option>\
                                                    <option value='pequeno'>Small</option>\
                                                    <option value='medio'>Medium</option>\
                                                    <option value='grande'>Big</option>\
                                                </select>\
                                            </div>\
                                            <div class='col-md-2'>\
                                                <input type='submit' class='btn btn-success' value='Update' id='atualizar'>\
                                                <a class= 'btn btn-danger' href='/clientes/deleta-pet/" + data['pets'][i]['id'] + "'>Delete</a>\
                                            </div>\
                                        </div>\
                                    </form>"
        }
    })
}

function update_cliente() {
    nome = document.getElementById('att-nome').value
    sobrenome = document.getElementById('att-sobrenome').value
    email = document.getElementById('att-email').value
    cpf = document.getElementById('att-cpf').value
    id = document.getElementById('id').value

    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    fetch('/clientes/atualiza-cliente/' + id, {
        method: 'POST',
        headers:{'X-CSRFToken' : csrf_token},
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
        })
    }).then(result => result.json()).then(function(data){
        if(data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            console.log('Dados alterados com sucesso!')
        }else{
            console.log('Ocorreu algum erro!')
        }
    })
}

function deleteRow(button) {
    let row = button.parentNode.parentNode; // Get the row containing the button
    console.log(row)
    row.parentNode.removeChild(row); // Remove the row
}

function filter_table() {
    let input, table, tr, td, i, txtValue;

    input = document.getElementById('filter').value;
    table = document.getElementById('services_list');
    tr = table.getElementsByTagName('tr');

    if (input == 'ALL') {
        for (i = 1; i < tr.length; i++) {
            tr[i].style.display = "";
        }
    } else {
        // Looping through all table rows, hiding those that don't match the search query
        for (i = 1; i < tr.length; i++) {
            td = tr[i].getElementsByTagName('td')[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.indexOf(input) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}