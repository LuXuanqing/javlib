'use strict'

// HTML结构： div#app-container 插入到 div.socialmedia之前
const appContainer = document.createElement('div')
appContainer.setAttribute('id', 'app-container')
const target = document.querySelector('div.socialmedia')
target.parentElement.insertBefore(appContainer, target)


// 把app的html插入到 #app-container
fetch(`http://localhost:5000/content`)
    .then(res => res.text())
    .then(text => {
        document.querySelector('#app-container').innerHTML = text
        console.info('Inserted HTML')
        initVue()
    })
    .catch(err => console.error(err))


function initVue() {
    new Vue({
        el: '#app',
        data: {
            id: '',
            genres: [],
            casts: [],
            lastVisit: {},
            imgs: {},
            imgIdx: 0,
            isShowImg: false,
        },
        methods: {
            showThisImg: function (img) {
                this.isShowImg = true
                this.imgIdx = this.imgs.indexOf(img)
            },
            nextImg: function () {
                if (this.imgIdx < this.imgs.length - 1) {
                    this.imgIdx += 1
                }
            },
            previousImg: function () {
                if (this.imgIdx > 0) {
                    this.imgIdx -= 1
                }
            },
            getPreview: function () {
                //TODO update this methods
            }
        },
        created: function () {
            //get ID
            this.id = document.querySelector('#video_id td.text').innerText
            console.info(`Got id: ${this.id}`)

            //get casts and genres
            function getList(query) {
                let list = []
                let spans = document.querySelectorAll(query)
                spans.forEach(span => {
                    if (span.querySelector('.alias')) {
                        let name = span.querySelector('.star').innerText
                        let alias = span.querySelector('.alias').innerText
                        list.push(`${name}(${alias})`)
                    } else {
                        list.push(span.innerText)
                    }
                })
                return list
            }

            this.casts = getList('#video_cast span.cast')
            console.info(`Got casts: ${this.casts}`)
            this.genres = getList('#video_genres span.genre')
            console.info(`Got genres: ${this.genres}`)

            // post casts&genres then get imgs&lastVisit
            let data = {
                genres: this.genres,
                cast: this.casts
            }
            fetch(`http://localhost:5000/api/av/${this.id}`, {
                method: 'POST',
                body: JSON.stringify(data), // data can be `string` or {object}!
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then(response =>
                response.json().then(data => ({
                        data: data,
                        status: response.status
                    })
                ).then(res => {
                    console.log(res.status, res.data)
                    this.imgs = res.data.imgs
                    this.lastVisit = res.data.lastVisit
                }))
                .catch(error => console.log(error))

        }
    })

}