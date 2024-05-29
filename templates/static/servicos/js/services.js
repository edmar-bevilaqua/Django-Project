function update_list_services() {
    client_id = document.getElementById('filter').value

    data = new FormData()
    data.append('client_id', client_id)

    fetch('/servicos/update_list/', {
        method:"POST",
        body: data
    }).then(response => response.json()).then(function(data){
        table = document.getElementById('services_list')
        html_text = ""

        table.innerHTML = "<thead>\
                                <tr>\
                                <th scope='col'>#</th>\
                                <th scope='col'>Title</th>\
                                <th scope='col'>Client</th>\
                                <th scope='col'>Finished</th>\
                                <th scope='col'>Identifier</th>\
                                <th scope='col'>Total Price</th>\
                                </tr>\
                            </thead>"
        if(data['service_pks'] !== undefined){
            for(i=0; i<data['service_pks'].length; i++){
                if(data['service_fields'][i]['finished'] == true){
                    html_text += "<tr>\
                                        <th scope='row'>"+ data['service_pks'][i] +"</th>\
                                        <td>"+ data['service_fields'][i]['title'] +"</td>\
                                        <td>"+ data['client_name'] +"</td>\
                                        <td>\
                                            <span class='badge badge-success'>Finalizado</span>\
                                        </td>\
                                        <td>"+ data['service_fields'][i]['identifier'] +"</td>\
                                        <th scope='row'>R$ "+ data['total_price'][i] +"</th>\
                                    </tr>"
                } else {
                    html_text += "<tr>\
                                        <th scope='row'>"+ data['service_pks'][i] +"</th>\
                                        <td>"+ data['service_fields'][i]['title'] +"</td>\
                                        <td>"+ data['client_name'] +"</td>\
                                        <td>\
                                            <span class='badge badge-info'>Em Andamento</span>\
                                        </td>\
                                        <td>"+ data['service_fields'][i]['identifier'] +"</td>\
                                        <th scope='row'>R$ "+ data['total_price'][i] +"</th>\
                                    </tr>"
                }
            }
        }
        table.innerHTML += "<tbody>" + html_text + "</tbody>"
    })
}