alert('loaded 2')
// 图片显示的容器
const div_test = document.createElement('div')
div_test.innerText = '{{ message }}'
div_test.setAttribute('id', 'app')
const div_videoimages = document.querySelector('#videoimages')
div_videoimages.parentElement.insertBefore(div_test, div_videoimages)
// 预览图
const img_preview = document.createElement('img')
img_preview.setAttribute

var app = new Vue({
    el: '#app',
    data: {
        message: 'hello vue'
    }
})