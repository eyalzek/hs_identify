var a = [],
    images = $(".visual-image-cell a img"),
    names = $(".visual-details-cell h3 a");

for (var i = names.length - 1; i >= 0; i--) {
    var temp = {};
    temp["url"] = images.get(i).src;
    temp["name"] = names.get(i).text;
    a.push(temp);
};
