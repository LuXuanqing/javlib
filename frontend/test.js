// import Vue from "./bower_components/vue/types";

// const inputBox = document.querySelector('#bangou')
// const infoBox = document.querySelector('#preview')
// const searchBtn = document.querySelector('#getp')

// searchBtn.addEventListener('click', getp)

// function getp() {
//     let bangou = inputBox.value
//     url = 'http://localhost:5000/info/' + bangou
//     axios.get(url)
//         .then(function (response) {
//             console.log(response)
//             infoBox.innerText = response.data[0].full
//         })
//         .catch(function (error) {
//             console.log(error);
//         });
// }

var app = new Vue({
    el: '#app',
    data: {
        bangou: 'ekdv-174',
        pics: [
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-1.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-1.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 1"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-2.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-2.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 2"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-3.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-3.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 3"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-4.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-4.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 4"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-5.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-5.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 5"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-6.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-6.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 6"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-7.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-7.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 7"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-8.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-8.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 8"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-9.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-9.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 9"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-10.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-10.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 10"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-11.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-11.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 11"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-12.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-12.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 12"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-13.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-13.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 13"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-14.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-14.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 14"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-15.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-15.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 15"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-16.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-16.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 16"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-17.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-17.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 17"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-18.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-18.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 18"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-19.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-19.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 19"
            },
            {
                "full": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147jp-20.jpg",
                "thumb": "https://pics.dmm.co.jp/digital/video/49ekdv00147/49ekdv00147-20.jpg",
                "title": "EKDV-147 NON STOP ORGASM \u30dd\u30eb\u30c1\u30aa\u30a8\u30f3\u30c9\u30eb\u30d5\u30a3\u30f3 \u6625\u54b2\u3042\u305a\u307f \u6deb\u6b32\u66b4\u8d70 - \u6a23\u54c1\u5716\u50cf - 20"
            }
        ]
    },
    methods: {
        getInfo: function() {
            url = 'http://localhost:5000/info/' + this.bangou
            axios.get(url)
                .then(function (response) {
                    this.pics = response.data
                    console.log(this.pics)
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    }
})