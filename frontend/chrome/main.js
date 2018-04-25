// 图片显示的容器
var div_mypreview = document.createElement('div')
div_mypreview.setAttribute('id', 'myapp')
var div_videoimages = document.querySelector('#videoimages')
div_videoimages.parentElement.insertBefore(div_mypreview, div_videoimages)
// 预览图
div_mypreview.innerHTML = '<a target="view_window" v-for="pic in pics" :href="pic.full"><img :src="pic.thumb" :title="pic.title"></a>'


var app = new Vue({
    el: '#myapp',
    data: {
        message: 'hello vue',
        bangou: '',
        pics: []
    },
    created: function() {
        // get bangou
        let div_id = document.querySelector('#video_id')
        let bangou = div_id.querySelector('td.text').innerText
        this.bangou = bangou
        //get pics
        url = 'http://localhost:5000/info/' + this.bangou
        axios.get(url)
            .then(response => {
                this.pics = response.data
                console.log(this.pics)
            })
            .catch(error => {
                console.log(error);
            })
    }
})