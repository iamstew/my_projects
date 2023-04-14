function onEntry(entry) {
    entry.forEach(change => {
        change.isIntersecting ? change.target.classList.add('show') : null
    });
}

let options = {
    threshold: [0.5]
};
let observer = new IntersectionObserver(onEntry, options);
var elements = document.querySelectorAll(".animation");
console.log(elements)

for (let elm of elements) {
    observer.observe(elm);
}