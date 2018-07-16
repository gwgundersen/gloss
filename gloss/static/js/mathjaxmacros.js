MathJax.Hub.Config({
    TeX: {
        Macros: {
            argmax: ["\\arg\\!\\max #1", 1],
            argmin: ["\\arg\\!\\min #1", 1]
        }
    }
});

MathJax.Ajax.loadComplete("/static/js/mathjaxmacros.js");