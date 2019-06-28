'use strict'
// HTML结构： div#app-container 插入到 div.socialmedia之前
const appContainer = document.createElement('div')
appContainer.setAttribute('id', 'app-container')
const target = document.querySelector('h4#mag-submit-show')
target.parentElement.insertBefore(appContainer, target)

// 把app的html插入到 #app-container
axios(`http://localhost:5000/content/javbus`)
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
            lastVisit: {},
            imgs: [],
            isDislike: false,
            isNeedHd: false
        },
        computed: {
            timeFromNow: function () {
                return moment(Date.parse(this.lastVisit.timestamp)).fromNow()
            },
            sitename: function () {
                if (!this.lastVisit.site) return null
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
            this.id = document.querySelector('.info p:first-of-type span:nth-of-type(2)').innerText
            console.info(`Got id: ${this.id}`)

            //get imgs
            let samples = document.querySelectorAll('.sample-box')
            samples.forEach(sample => {
                let p = {
                    full: sample.href,
                    thumb: sample.querySelector('img').src,
                    title: sample.querySelector('img').title
                }
                this.imgs.push(p)
            })
            console.log(this.imgs)
            // moment localization
            moment.locale('zh-CN')
            // post casts&genres then get imgs&lastVisit
            axios.post(`http://localhost:5000/api/javbus/${this.id}`, {
                imgs: this.imgs
            })
                .then(res => {
                    console.info(res)
                    this.lastVisit = res.data.lastVisit
                    this.isDislike = res.data.isDislike
                    this.isNeedHd = res.data.isNeedHd
                })
                .catch(err => console.error(err))
        }
    })

}




