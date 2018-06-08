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
        initVue()
    })
    .catch(err => console.log(err))


function initVue() {

    let app = new Vue({
        el: '#app',
        data: {
            id: '',
            info: {},
            infoOnThisPage: {},
            curImg: {
                index: 0,
                show: false,
                img: {}
            },
        },
        watch: {
            'curImg.index': function () {
                console.log('index changed')
                this.curImg.img = this.info.preview[this.curImg.index]
            }
        },
        computed: {
            formatedTime: function () {
                let time_python = this.info.last_visit
                if (time_python == -2) {
                    return '以前从来没看过'
                }
                let timestamp = parseInt(time_python * 1000)
                let date = new Date(timestamp)
                return `${date.getFullYear()}/${date.getMonth()}/${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
            },
            javbusLink: function () {
                return `https://www.javbus6.pw/${this.id}`
            },
            hasPreview: function () {
                if (!this.info.preview) return false
                return this.info.preview.length > 0
            },
            atFirst: function () {
                return this.curImg.index == 0
            },
            atLast: function () {
                return this.curImg.index == this.info.preview.length-1
            }
        },
        methods: {
            showThisImg: function (img) {
                this.curImg.img = img
                this.curImg.show = true
                this.curImg.index = this.info.preview.indexOf(img)
            },
            closeImg: function () {
                this.curImg.show = false
            },
            nextImg: function () {
                if (this.curImg.index < this.info.preview.length - 1) {
                    this.curImg.index += 1
                }
            },
            previousImg: function () {
                if (this.curImg.index > 0) {
                    this.curImg.index -= 1
                }
            },
            getInfo: function () {
                fetch(`http://localhost:5000/info/${this.id}`)
                    .then(res => res.json())
                    .then(myjson => {
                        this.info = myjson
                        this.postInfo()
                    })
                    .catch(err => console.log(err))
                console.log('get info ok')
            },
            getPreview: function () {
                fetch(`http://localhost:5000/preview/${this.id}?force=1`)
                    .then(res => res.json())
                    .then(myjson => this.info.preview = myjson)
                    .catch(err => console.log(err))
            },
            getInfoOnThisPage: function () {
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
                this.infoOnThisPage = {
                    cast: getList('#video_cast span.cast'),
                    genres: getList('#video_genres span.genre')
                }
                console.log('get info on this page ok')
            },
            getId: function () {
                this.id = document.querySelector('#video_id td.text').innerText
            },
            postInfo: function () {
                /**
                 * 检测是否为null或空数组
                 * @param {null, Array} val 
                 */
                function isEmpty(val) {
                    if (val === null) return true
                    if (Array.isArray(val)) return val.length == 0
                    return !val
                }

                let data = {
                    genres: [],
                    cast: []
                }
                let postGenres = isEmpty(this.info.genres) && !isEmpty(this.infoOnThisPage.genres)
                let postCast = isEmpty(this.info.cast) && !isEmpty(this.infoOnThisPage.cast)
                if (postGenres) {
                    data.genres = this.infoOnThisPage.genres
                }
                if (postCast) {
                    data.cast = this.infoOnThisPage.cast
                }
                if (postGenres || postCast) {
                    fetch(`http://localhost:5000/info/${this.id}`, {
                            method: 'POST',
                            body: JSON.stringify(data), // data can be `string` or {object}!
                            headers: new Headers({
                                'Content-Type': 'application/json'
                            })
                        }).then(res => res.json())
                        .then(json => {
                            console.log('post success:', json.success)
                            this.info.genres = json.genres
                            this.info.cast = json.cast
                        })
                        .catch(error => console.error('Error:', error))
                } else {
                    console.log('no need to post')
                }
            }
        },
        created: function () {
            this.getId()
            this.getInfoOnThisPage()
            this.getInfo()
        }
    })

}