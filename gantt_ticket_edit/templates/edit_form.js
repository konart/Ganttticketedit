var options  = $options;
var has_permission = $has_permission;

for (var j = 0; j <options.length; j++) { 
  options[j]=options[j].replace(/-/g,"").replace(/_/g,"")
}

function createRequestObject() {
    try { return new XMLHttpRequest() }
    catch(e) {
      try { return new ActiveXObject('Msxml2.XMLHTTP') }
      catch(e) {
        try { return new ActiveXObject('Microsoft.XMLHTTP') }
        catch(e) { return null; }
      }
    }
  }

var parser=new DOMParser();


jQuery(document).ready(function($) {

$(".tip").each(function(){
  if (has_permission) {
  string_link = $(this).attr('href');
  string_link = string_link.substring(string_link.indexOf("/",9)+1);
  $(this).after('<a href="#" id="'+string_link+'" class="edit">Edit</a>')
  }
});

$("h1").text("New tickets").before('<div id="ticket_editor"></div>');

$('body').append('<div id="loader"><span>Идет отправка, подождите..</span></div>');
$("#loader").css({'position':'fixed','display':'none','top':'0','left':'0','height':'100%','width':'100%','background':'#ccc','opacity':'.9'})
$("#loader span").css({'display':'block','position':'absolute','right':'4px','top':'4px','color':'#fff','background':'#C71D72','padding':'5px 10px','-webkit-border-radius': '5px', '-moz-border-radius': '5px','border-radius': '5px', 'cursor':'default'})
$('#loader').ajaxSend(function(event, jqxhr, settings){ if (settings.type == "POST") {$(this).show() } })
  .ajaxStop(function(){$(this).hide()});

window.cont = $('#ticket_editor')[0];

  $(".edit").click(function() {
      var ticket_link = "http://"+location.host+"/Planing/ticket/"+$(this).attr('id');
      create(ticket_link);
      if ($(this).html()=="Edit") {
        $(this).html("Close");
        $(".edit").not(this).html("Edit");
        $('#ticket_editor').show();
      } else {
        $(this).html("Edit");
        $('#ticket_editor').hide();
      }
  });


//var http = createRequestObject(); // создаем ajax-объект


function create(ticket_link) {

  if($(cont).html() == "") {
      var http = $.ajax({type: "GET", url: ticket_link, dataType: "html", success: function(data) {
        if(http.readyState == 4) {
          var xmlDoc=parser.parseFromString(data,"text/xml");
          var tds = xmlDoc.getElementById("propertyform");  //переписать на jquery

            fors = $(tds).find(("[for]"))

            for (var i = 0; i <fors.length; i++) {
              if ($.inArray(fors[i].getAttribute("for").replace(/-/g,"").replace(/_/g,""),options) > -1 ) {
                  $(fors[i].parentNode).next().remove();
                  $(fors[i].parentNode).remove()
              }
            }

            $(cont).append(tds);

                $('#propertyform').submit(function(event){
                  event.preventDefault();
                  var edit_link = "http://"+location.host+$(this).attr("action"); 
                  $.post(edit_link, $(this).serialize(), function() { $(cont).empty(); create(ticket_link); })
                });

        }
      }, error: function(data) {
          document.location = ticket_link;
      }});


   //   document.location = link; // если ajax-объект не удается создать, просто перенаправляем на адрес


  } else {
    $(cont).empty();
    $('#ticket_editor').hide();
    create(ticket_link);
    }

}

});