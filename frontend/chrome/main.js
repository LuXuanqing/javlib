// HTML结构： div#app-container 插入到 div.socialmedia之前
const appContainer = document.createElement('div')
appContainer.setAttribute('id', 'app-container')
target = document.querySelector('div.socialmedia')
target.parentElement.insertBefore(appContainer, target)


// 把app的html插入到 #app-container
axios.get('http://localhost:5000/content')
    .then(res => {
        // console.log(res)
        document.querySelector('#app-container').innerHTML = res.data
        initVue()
    })
    .catch(err => console.log(err))

    function initVue() {
        let app = new Vue({
            el: '#app',
            data: {
                id: '',
                currentPic: {},
                showPreview: false,
                info: {}
            },
            methods: {
                getInfo: function () {
                    url = 'http://localhost:5000/info/' + this.id
                    axios.get(url)
                        .then(function (response) {
                            this.info = response.data
                        })
                        .catch(function (error) {
                            console.log(error);
                        })
                },
                showThisPic: function (pic) {
                    this.showPreview = true
                    this.currentPic = pic
                },
                closePreview: function () {
                    this.showPreview = false
                }
            },
            created: function() {
                let id = document.querySelector('#video_id td.text').innerText
                this.id = id
                let url = 'http://localhost:5000/info/' + this.id
                axios.get(url)
                    .then(res => {
                        this.info = res.data
                    })
                    .catch(err => console.log(err))
            }
        })
    }