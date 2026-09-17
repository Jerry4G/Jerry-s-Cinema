(function () {
    const originalOpen = window.open;

    window.open = function (url, target, features) {
        console.log("Popup bloquée :", url);
        return null;
    };
})();