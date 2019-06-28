'use strict'

// HTML结构： div#app-container 插入到 div.socialmedia之前
const appContainer = document.createElement('div')
appContainer.setAttribute('id', 'app-container')
const target = document.querySelector('div.socialmedia')
target.parentElement.insertBefore(appContainer, target)


// 把app的html插入到 #app-container
axios(`http://localhost:5000/content/javlib`)
    .then(res => {
        document.querySelector('#app-container').innerHTML = res.data
        console.info('Inserted HTML')
        init()
    })
    .catch(err => console.error(err))


function init() {
    new Vue({
        el: '#app',
        data: {
            id: '',
            genres: [],
            casts: [],
            lastVisit: {},
            imgs: [],
            imgIdx: 0,
            isShowImg: false,
            isDislike: false,
            isNeedHd: false
        },
        computed: {
            timeFromNow: function () {
                return moment(Date.parse(this.lastVisit.timestamp)).fromNow()
            },
            sitename: function () {
                if (this.lastVisit.site.indexOf('javbus') > -1) {
                    return 'JavBus'
                } else if (this.lastVisit.site.indexOf('javlibrary') > -1) {
                    return 'JavLibrary'
                } else {
                    return this.lastVisit.site
                }
            }
        },
        methods: {
            showThisImg: function (img) {
                this.isShowImg = true
                this.imgIdx = this.imgs.indexOf(img)
            },
            nextImg: function () {
                console.log('next')
                if (this.imgIdx < this.imgs.length - 1) {
                    this.imgIdx += 1
                }
            },
            previousImg: function () {
                console.log('pre')
                if (this.imgIdx > 0) {
                    this.imgIdx -= 1
                }
            },
            getPreview: function () {
                //TODO update this methods
            },
            disLike: function () {
                axios.put(`http://localhost:5000/api/av/WANZ-801/dislike`, {
                    isDislike: !this.isDislike
                })
                    .then(res => {
                        this.isDislike = !this.isDislike
                    })
                    .catch(err => console.error(err))
            },
            needHd: function () {
                axios.put(`http://localhost:5000/api/av/WANZ-801/needhd`, {
                    isNeedHd: !this.isNeedHd
                })
                    .then(res => {
                        this.isNeedHd = !this.isNeedHd
                    })
                    .catch(err => console.error(err))
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
                        let name = span.querySelector('.star').innerText.trim()
                        let alias = span.querySelector('.alias').innerText.trim()
                        list.push(`${name}(${alias})`)
                    } else {
                        list.push(span.innerText.trim())
                    }
                })
                return list
            }
            this.casts = getList('#video_cast span.cast')
            console.info(`Got casts: ${this.casts}`)
            this.genres = getList('#video_genres span.genre')
            console.info(`Got genres: ${this.genres}`)
            // moment localization
            moment.locale('zh-CN')
            // post casts&genres then get imgs&lastVisit
            axios.post(`http://localhost:5000/api/javlib/${this.id}`, {
                genres: this.genres,
                cast: this.casts
            })
                .then(res => {
                    console.info(res)
                    this.imgs = res.data.imgs
                    this.lastVisit = res.data.lastVisit
                    this.isDislike = res.data.isDislike
                    this.isNeedHd = res.data.isNeedHd
                })
                .catch(err => console.error(err))
        }
    })

}