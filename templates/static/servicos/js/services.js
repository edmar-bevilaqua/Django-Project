function update_list_services() {
    client_id = document.getElementById('filter').value

    data = new FormData()
    data.append('client_id', client_id)

    fetch('/servicos/update_list/', {
        method:"POST",
        body: data
    }).then(response => response.json()).then(function(data){
        console.log(data)
    })
}