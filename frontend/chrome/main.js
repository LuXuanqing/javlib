'use strict'

// HTML结构： div#app-container 插入到 div.socialmedia之前
const appContainer = document.createElement('div')
appContainer.setAttribute('id', 'app-container')
const target = document.querySelector('div.socialmedia')
target.parentElement.insertBefore(appContainer, target)


// 把app的html插入到 #app-container
axios.get('http://localhost:5000/content')
    .then(res => {
        document.querySelector('#app-container').innerHTML = res.data
        initVue()
    })
    .catch(err => console.log(err))


function initVue() {

    let app = new Vue({
        el: '#app',
        data: {
            info: {},
            preview: [],
            download: [],
            lastVisit: '',
            curImg: {},
            showImg: false,
        },
        computed: {
            getLastVisit: function () {
                // let timestamp = parseInt(this.lastVisit * 1000)
                // let date = new Date(timestamp)
                // rst = `${date.getFullYear()}/${date.getMonth()}/${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
                // console.log(rst)
                console.log('ok')
                return this.lastVisit
            }
        },
        methods: {
            showThisImg: function (img) {
                this.curImg = img
                this.showImg = true
            },
            closeImg: function () {
                this.showImg = false
            },
            getInfo: function () {
                function getList(query) {
                    let list = []
                    let spans = document.querySelectorAll(query)
                    spans.forEach(span => {
                        if (span.querySelector('.alias')) {
                            let name = span.querySelector('.star').innerText
                            let alias = span.querySelector('.alias').innerText
                            list.push(name + '(' + alias + ')')
                        } else {
                            list.push(span.innerText)
                        }
                    })
                    return list
                }
                this.info = {
                    'id': document.querySelector('#video_id td.text').innerText,
                    'cast': getList('#video_cast span.cast'),
                    'genres': getList('#video_genres span.genre')
                }
            },
            getPreview: function (id) {
                axios.get(`http://localhost:5000/preview/${id}`)
                    .then(res => this.preview = res.data)
                    .catch(err => console.log(err))
            },
            getDownload: function (id) {
                axios.get(`http://localhost:5000/download/${id}`)
                    .then(res => this.download = res.data)
                    .catch(err => console.log(err))
            },
            postInfo: function () {
                // get请求：检查是否有info
                axios.get('http://localhost:5000/info/' + this.info.id)
                    .then(res => {
                        // 如果没有info，发送post请求提交数据
                        if (!res.data) {
                            axios.post('http://localhost:5000/info/' + this.info.id, {
                                    genres: this.info.genres,
                                    cast: this.info.cast
                                })
                                .then(res => console.log(res.data))
                                .catch(err => console.log(err))
                        }
                    })
                    .catch(err => console.log(err))
            },
            getLastVisit: function (id) {
                axios.get(`http://localhost:5000/log/${id}`)
                    .then(res => this.lastVisit = res.data)
                    .catch(err => console.log(err))
            }
        },
        created: function () {
            this.getInfo()
            this.getPreview(this.info.id)
            this.getDownload(this.info.id)
            this.getLastVisit(this.info.id)
            // this.postInfo()
        }
    })

}