//const { header } = require("express/lib/request")

function add_pet(){
    container = document.getElementById('form-pet')
    html = "<br> <div class='row'> <div class='col-md'> <label for='pet'>Nome do Pet:</label><input type='text' placeholder='Nome do Pet' class='form-control' name='pet'> </div> <div class='col-md'> <label for='data-nascimento'>Data de Nascimento:</label><input type='date' placeholder='DD/MM/AAAA' class='form-control' name='data-nascimento'> </div> <div class='col-md'> <label for='porte'>Porte do Pet:</label> <select name='porte' class='form-control'><option value='pequeno'>Pequeno</option><option value='medio'>Médio</option><option value='grande'>Grande</option></select> </div> </div>"

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

    console.log(csrf_token.value)
    console.log(data)
    fetch('/clientes/atualizar_cliente', {
        method:'POST',
        headers:{'X-CSRFToken' : csrf_token},
        body: data
    }).then(response => response.json()).then(function(data){
        console.log("teste")
    })
}