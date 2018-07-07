$('#switch2 a').on('click',function(e) {
    e.preventDefault();
    $('img').fadeOut('fast');
    var pic1_src = $('#pic1').attr('src')
    var new1_src = (parseInt(pic1_src.match(/\d/)[0])+1).toString()
    new1_src = pic1_src.replace(pic1_src.match(/\d/), new1_src)
    $('#pic1').attr('src', new1_src)
    var pic2_src = $('#pic2').attr('src')
    var new2_src = (parseInt(pic2_src.match(/\d/)[0])+1).toString()
    new2_src = pic2_src.replace(pic2_src.match(/\d/), new2_src)
    $('#pic2').attr('src', new2_src)
    $('img').fadeIn();
    // $('#content').reload();
});
$('#switch1 a').on('click',function(e) {
    e.preventDefault();
    $('img').fadeOut('fast');
    var pic1_src = $('#pic1').attr('src')
    var new1_src = (parseInt(pic1_src.match(/\d/)[0])-1).toString()
    new1_src = pic1_src.replace(pic1_src.match(/\d/), new1_src)
    $('#pic1').attr('src', new1_src)
    var pic2_src = $('#pic2').attr('src')
    var new2_src = (parseInt(pic2_src.match(/\d/)[0])-1).toString()
    new2_src = pic2_src.replace(pic2_src.match(/\d/), new2_src)
    $('#pic2').attr('src', new2_src)
    $('img').fadeIn();
    // $('#content').reload();
});
