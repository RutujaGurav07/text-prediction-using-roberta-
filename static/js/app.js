var data = []
var token = ""
var p_text=""

jQuery(document).ready(function () {
    closePopUp();

    var slider = $('#max_words')
    slider.on('change mousemove', function (evt) {
        $('#label_max_words').text('Top k words: ' + slider.val())
    })

    var slider_mask = $('#max_words_mask')
    slider_mask.on('change mousemove', function (evt) {
        $('#label_max_words').text('Top k words: ' + slider_mask.val())
    })

    $('#input_text').on('keyup', function (e) {

        if (e.key == ' ') {
            $.ajax({
                url: '/get_end_predictions',
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    "input_text": $('#input_text').val(),
                    "top_k": slider.val(),
                }),
                beforeSend: function () {
                    $('.overlay').show()
                },
                complete: function () {
                    $('.overlay').hide()
                }
            }).done(function (jsondata, textStatus, jqXHR) {
                // console.log(jsondata['roberta'])
                append_data(jsondata['roberta'])


                

                $('#text_roberta').val(jsondata['roberta'])
            }).fail(function (jsondata, textStatus, jqXHR) {
                console.log(jsondata)
            });
        }
    })

    $('#btn-process').on('click', function () {
        $.ajax({
            url: '/get_mask_predictions',
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "input_text": $('#mask_input_text').val(),
                "top_k": slider_mask.val(),
            }),
            beforeSend: function () {
                $('.overlay').show()
            },
            complete: function () {
                $('.overlay').hide()
            }
        }).done(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $('#mask_text_roberta').val(jsondata['roberta'])
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
        });
    })
   
})
function append_data(data) {
    var newpost = $('#newpost');
    var txtarea = document.getElementById("input_text");
    console.log(data)
    var words = data.split("\n");
    console.log(words);
    console.log(typeof (data))

    var start = txtarea.selectionStart;
    var finish = txtarea.selectionEnd;
    var list = "<ul class = 'pred_list' >"
    for (let i of words) {
        list += `<li class ="P_values">${i}</li>`;

    }
    list += "</ul>";

    document.getElementById("newpost").innerHTML = list;

    newpost.offset(getCursorXY(txtarea, start, 20)).show();
    document.querySelector('ul').addEventListener('click', function(e) {   // 1.
        var selected;
        
        if(e.target.tagName === 'LI') {                                      // 2.
          selected= document.querySelector('li.selected');                   // 2a.
          if(selected) selected.className= '';                               // "
          e.target.className= 'selected';                                    // 2b.
          p_text=e.target.innerText;
          document.getElementById("input_text").value += p_text;
          closePopUp();
        }
          
        
      });


}


function getSel() {
    // obtain the object reference for the textarea>
    var txtarea = document.getElementById("input_text");
    console.log(txtarea)
    // obtain the index of the first selected character
    var start = txtarea.selectionStart;
    // obtain the index of the last selected character
    var finish = txtarea.selectionEnd;
    //obtain all Text
    var allText = txtarea.value;
    // obtain the selected text
    var sel = Array(finish - start + 1).join("*");
    //append te text;
    var newText = allText.substring(0, start) + sel + allText.substring(finish, allText.length);
    txtarea.value = newText;
    $('#newpost').offset({ top: 0, left: 0 }).hide();
   
}
function closePopUp() {
    $('#newpost').offset({ top: 0, left: 0 }).hide();
}
const getCursorXY = (input, selectionPoint, offset) => {
    const {
        offsetLeft: inputX,
        offsetTop: inputY,
    } = input
    // create a dummy element that will be a clone of our input
    const div = document.createElement('div')
    // get the computed style of the input and clone it onto the dummy element
    const copyStyle = getComputedStyle(input)
    for (const prop of copyStyle) {
        div.style[prop] = copyStyle[prop]
    }
    // we need a character that will replace whitespace when filling our dummy element 
    // if it's a single line <input/>
    const swap = '.'
    const inputValue = input.tagName === 'INPUT' ? input.value.replace(/ /g, swap) : input.value
    // set the div content to that of the textarea up until selection
    const textContent = inputValue.substr(0, selectionPoint)
    // set the text content of the dummy element div
    div.textContent = textContent
    if (input.tagName === 'TEXTAREA') div.style.height = 'auto'
    // if a single line input then the div needs to be single line and not break out like a text area
    if (input.tagName === 'INPUT') div.style.width = 'auto'
    // create a marker element to obtain caret position
    const span = document.createElement('span')
    // give the span the textContent of remaining content so that the recreated dummy element 
    // is as close as possible
    span.textContent = inputValue.substr(selectionPoint) || '.'
    // append the span marker to the div
    div.appendChild(span)
    // append the dummy element to the body
    document.body.appendChild(div)
    // get the marker position, this is the caret position top and left relative to the input
    const { offsetLeft: spanX, offsetTop: spanY } = span
    // lastly, remove that dummy element
    // NOTE:: can comment this out for debugging purposes if you want to see where that span is rendered
    document.body.removeChild(div)
    // return an object with the x and y of the caret. account for input positioning 
    // so that you don't need to wrap the input
    return {
        left: inputX + spanX,
        top: inputY + spanY + offset,
    }
}


