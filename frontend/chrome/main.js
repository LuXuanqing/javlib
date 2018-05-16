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
            info: {},
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
        created: function () {
            // get info
            function getList(query) {
                var list = []
                spans = document.querySelectorAll(query)
                spans.forEach(span => {
                    if (span.querySelector('.alias')) {
                        let name = span.querySelector('.star').innerText
                        let alias = span.querySelector('.alias').innerText
                        list.push(name+'('+alias+')')
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
            console.log(this.info)
            // get preview
            let base_url = 'http://localhost:5000/'
            axios.get(base_url + 'preview/' + this.info.id, {
                    params: {
                        'cast': JSON.stringify(this.info.cast),
                        'genres': JSON.stringify(this.info.genres)
                    }
                })
                .then(res => {
                    // console.log(res.data)
                    this.preview = res.data
                })
                .catch(err => console.log(err))
            // get download link
            axios.get(base_url + 'download/' + this.info.id)
                .then(res => {
                    // console.log(res.data)
                    this.download = res.data
                })
                .catch(err => console.log(err))
        }
    })
}