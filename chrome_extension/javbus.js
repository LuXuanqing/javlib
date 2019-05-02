'use strict'
let id = document.querySelector('.info p:first-of-type span:nth-of-type(2)').innerText
if (id) {
    console.log(`id: ${id}`)
} else {
    console.log('cant get id')
}
let preview = []
let samples = document.querySelectorAll('.sample-box')
samples.forEach(sample => {
    let p = {
        full: sample.href,
        thumb: sample.querySelector('img').src,
        title: sample.querySelector('img').title
    }
    preview.push(p)
})
// 成功获取id和preview才POST
if (preview.length > 0 && id) {
    fetch(`http://localhost:5000/preview/${id}`, {
            method: 'POST',
            body: JSON.stringify(preview),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }).then(res => res.json())
        .then(json => console.log(`last visit: ${json.last_visit.timestamp}@${json.last_visit.domain}`))
        .catch(error => console.error('Error:', error))
}