alert('loaded 2')
// 图片显示的容器
var div_mypreview = document.createElement('div')
// div_mypreview.innerText = '{{ message }}'
div_mypreview.setAttribute('id', 'myapp')
var div_videoimages = document.querySelector('#videoimages')
div_videoimages.parentElement.insertBefore(div_mypreview, div_videoimages)
// 预览图
// div_mypreview.innerHTML = '<ul>{{ bangou }}</ul>'
div_mypreview.innerHTML = '<a v-for="pic in pics" v-bind:href="pic.full"><img v-bind:src="pic.thumb"></a>'


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