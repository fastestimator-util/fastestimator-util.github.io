window.MathJax = {
    tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
    },
    options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex"
    }
};

// document$.subscribe(() => {
//     MathJax.typesetPromise()
// })

// tsParticles
//     .loadJSON("tsparticles", "stylesheets/tsparticles.json")
//     .then(container => {
//         console.log("callback - tsparticles config loaded");
//     })
//     .catch(error => {
//         console.error(error);
//     });