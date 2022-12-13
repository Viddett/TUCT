

function glenn_test(arg) {
    alert("e du go eller denna e inte implementerad ännu");
    console.log("glenn_tese")
    console.log(arg)
}



async function get_tree_status(ip_adress) {
    console.log("GET TREE STATUS")
    var response = await fetch('http://' + ip_adress +'/state', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }//,
        //body: JSON.stringify({ "id": 78912 })
    })
        .then(response => response.json())
        //.then(response => console.log(JSON.stringify(response)))
    //response_json = response.json()
    //console.log(response_json)
    return response
    //yield response

}

function set_tree_status(ip_adress, obj) {

    // JSON.stringify({ "id": 78912 })

    fetch('http://' + ip_adress + '/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(obj)
    })
        .then(response => response.json())
        .then(response => console.log(JSON.stringify(response)))

}


