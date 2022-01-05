function toggleChoicesSection(type) {
    if (type == 1) {
        document.querySelector("#topics-group").style.display = 'block';
    } else {
        document.querySelector("#topics-group").style.display = 'none';
    }
}

function execWhenDocReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

execWhenDocReady(() => {
    const type = document.querySelector('#id_type').value;

    toggleChoicesSection(type);

    document.querySelector("#id_type").addEventListener('change', e => {
        toggleChoicesSection(e.target.value)
    });
})
