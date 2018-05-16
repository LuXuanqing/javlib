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
                download: [],
                preview: [],
                curImg: {},
                showImg: false,
            },
            methods: {
                showThisImg: function (img) {
                    console.log(img)
                    this.curImg = img
                    this.showImg = true
                },
                closeImg: function () {
                    this.showImg = false
                }
            },
            created: function() {
                // get id
                let id = document.querySelector('#video_id td.text').innerText
                this.id = id
                // get preview
                let base_url = 'http://localhost:5000/'
                axios.get(base_url + 'preview/' + id)
                    .then(res => {
                        // console.log(res.data)
                        this.preview = res.data
                    })
                    .catch(err => console.log(err))
                // get download link
                axios.get(base_url + 'download/' + id)
                    .then(res => {
                        // console.log(res.data)
                        this.download = res.data
                    })
                    .catch(err => console.log(err))
            }
        })
    }