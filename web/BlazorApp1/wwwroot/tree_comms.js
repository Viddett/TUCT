

function glenn_test(arg) {
    alert("e du go eller denna e inte implementerad ännu");
    console.log("glenn_tese")
    console.log(arg)
}

function get_tree_status(ip_adress) {
    console.log("GET TREE STATUS")

    return fetch('http://' + ip_adress + '/state', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    }).then(response => response.json())
        .then(response => JSON.stringify(response) )
}


function set_tree_status(ip_adress, obj) {

    console.log("SET TREE STATUS")
    console.log(obj)

    return fetch('http://' + ip_adress + '/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(obj)
    })
        .then(response => console.log(response))
        .then(response => response.json())
        .then(response => console.log(response))
        .then(response => JSON.stringify(response))
       
}


async function set_tree_status2(ip_adress, obj) {

    console.log("SET TREE STATUS")
    console.log(obj)

    const resp = await fetch('http://' + ip_adress + '/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(obj)
    })
    const res_obj = await resp.json()
    console.log(res_obj)
    return JSON.stringify(res_obj)


}


