$(function(){
    $("#file_upload").uploadify({
        'swf' : '/static/uploadify.swf',
        'uploader' : '/media/upload',
        'fileTypeExts' : '*.jpg',
        'formData' : {'id' : gallery['id'],
                      'dir' : gallery['dir']},
        'onQueueComplete' : function(queueData) {
            location.reload();
        },
    });
});

var title_value = null
var descr_value = null
$(document).ready(function(){
  
    $("img[rel]").overlay(); 
    //Invoke the edit prompts
    $('.edit_medium').click(function(){
        $(this).parent().siblings('.edit_title').slideUp();
        $(this).parent().siblings('.edit_descr').slideUp();
        $(this).parent().siblings('.edit_title').slideDown();
    });

    //Dimiss the edit prompts
    $('span.cancel').click(function(){
        $(this).parent().slideUp();
    });

    //Show the field for the medium description
    $('.edit_medium_next').click(function(){
        title_value = $(this).siblings('.title_value').val()
        $(this).parent().slideUp();
        $(this).parent().siblings('.edit_descr').slideDown();
    });

    //Submit changes to the application
    $('.edit_medium_done').click(function(){
        descr_value = $(this).siblings('.descr_value').val()
        var done_link = $(this);
        $(this).parent().slideUp();
        var medium_id = $(this).attr('id');
        $.ajax({
            type: "POST",
            url: "/media/update_ajax",
            data: { 'title': title_value, 'description': descr_value, 'id':medium_id }
        }).done(function() {
            done_link.parents('.simple_overlay').find('.medium_title').html(title_value)
            done_link.parents('.simple_overlay').find('div.medium_descr').html(descr_value)
            title_value = null
            descr_value = null
        }).fail(function() {
            done_link.parent().siblings('.edit_failed').slideDown();
        });
    });
    
    //Clear out the default value
    $('.input').click(function(){
        if ($(this).val().slice(0,14) == 'Please enter a')
            $(this).val('');
    });
    
    //Show the description over the image
    $('img.medium').mouseover(function(){
        $(this).siblings('div.medium_descr').slideDown();
    });
    $('img.medium').mouseout(function(){
        $(this).siblings('div.medium_descr').slideUp();
    });

    //Delete the image
    $('.delete_medium').click(function(){
        var medium_id = $(this).attr('id');
        var delete_link = $(this);
        var delete_check = confirm("Are you sure you want to delete this file")
        if (delete_check){
            $.ajax({
                type: "POST",
                url: "/media/delete",
                data: { 'id':medium_id }
            }).done(function() {
                var target_node = delete_link.parents('.media_container');
                target_node.find('div.media_thumb img[rel]').overlay().close()
                setTimeout(function() {target_node.detach()}, 800);
            }).fail(function() {
                delete_link.parent().siblings('.edit_failed').slideDown();
            });
        }
    });

    $('.rotate_r_medium').click(function(){
        var medium_id = $(this).attr('id');
        var rotate_link = $(this);
        $('.fence, .centerPopup').fadeIn('fast')
        $.ajax({
            type: "POST",
            url: ("/media/rotate/" + medium_id),
            data: { 'direction':-90}
        }).done(function() {
            var target_node_1 = rotate_link.parents('.simple_overlay').find('div img.medium');
            var target_node_2 = rotate_link.parents('.media_container').find('div.media_thumb img');
            old_src_1 = target_node_1.attr('src')
            old_src_2 = target_node_2.attr('src')
            d = new Date()
            $(target_node_1).attr('src', old_src_1+'?'+d.getTime())
            $(target_node_2).attr('src', old_src_2+'?'+d.getTime())
            $('.fence, .centerPopup').fadeOut('fast')
        }).fail(function() {
            $('.fence, .centerPopup').fadeOut('fast')
            rotate_link.parent().siblings('.edit_failed').slideDown();
        });
    });
    $('.rotate_l_medium').click(function(){
        var medium_id = $(this).attr('id');
        var rotate_link = $(this);
        $('.fence, .centerPopup').fadeIn('fast')
        $.ajax({
            type: "POST",
            url: ("/media/rotate/" + medium_id),
            data: { 'direction':90}
        }).done(function() {
            var target_node_1 = rotate_link.parents('.simple_overlay').find('div img.medium');
            var target_node_2 = rotate_link.parents('.media_container').find('div.media_thumb img');
            old_src_1 = target_node_1.attr('src')
            old_src_2 = target_node_2.attr('src')
            d = new Date()
            $(target_node_1).attr('src', old_src_1+'?'+d.getTime())
            $(target_node_2).attr('src', old_src_2+'?'+d.getTime())
            $('.fence, .centerPopup').fadeOut('fast')
        }).fail(function() {
            $('.fence, .centerPopup').fadeOut('fast')
            rotate_link.parent().siblings('.edit_failed').slideDown();
        });
    });
    $('.restore_medium').click(function(){
        var medium_id = $(this).attr('id');
        var restore_link = $(this);
        $('.fence, .centerPopup').fadeIn('fast')
        $.ajax({
            type: "POST",
            url: ("/media/restore/" + medium_id),
        }).done(function() {
            var target_node_1 = restore_link.parents('.simple_overlay').find('div img.medium');
            var target_node_2 = restore_link.parents('.media_container').find('div.media_thumb img');
            old_src_1 = target_node_1.attr('src')
            old_src_2 = target_node_2.attr('src')
            d = new Date()
            $(target_node_1).attr('src', old_src_1+'?'+d.getTime())
            $(target_node_2).attr('src', old_src_2+'?'+d.getTime())
            $('.fence, .centerPopup').fadeOut('fast')
        }).fail(function() {
            $('.fence, .centerPopup').fadeOut('fast')
            restore_link.parent().siblings('.edit_failed').slideDown();
        });
    });
});



