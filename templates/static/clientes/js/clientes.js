function add_pet(){
    container = document.getElementById('form-pet')
    html = "<br> <div class='row'> <div class='col-md'> <label for='pet'>Nome do Pet:</label><input type='text' placeholder='Nome do Pet' class='form-control' name='pet'> </div> <div class='col-md'> <label for='data-nascimento'>Data de Nascimento:</label><input type='date' placeholder='DD/MM/AAAA' class='form-control' name='data-nascimento'> </div> <div class='col-md'> <label for='porte'>Porte do Pet:</label> <select name='porte' class='form-control'><option value='pequeno'>Pequeno</option><option value='medio'>Médio</option><option value='grande'>Grande</option></select> </div> </div>"

    container.innerHTML += html
}