const inputBox = document.querySelector('#bango')
const infoBox = document.querySelector('#info')
const searchBtn = document.querySelector('#getp')

searchBtn.addEventListener('click', getp)

function getp() {
    let bango = inputBox.value
    url = 'http://localhost:5000/info/' + bango
    axios.get(url)
        .then(function (response) {
            console.log(response)
            infoBox.innerText = response.data[0].full
        })
        .catch(function (error) {
            console.log(error);
        });
}

