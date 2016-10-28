<script type="text/javascript">
 var renderer_zai30 = new marked.Renderer();
marked.setOptions({
    renderer: renderer_zai30,
    gfm: true,
    tables: true,
    breaks: true,//回车换成br
    pedantic: false,
    sanitize: true,
    smartLists: true,
    smartypants: false
});

//
function Editor(input, preview) {
    this.update = function () {
        //marked(input.value); 解析Markdown为HTML
        preview.innerHTML = marked(input.value);
    };
    input.editor = this;
    this.update();
};
var $markdown = function (id) { return document.getElementById(id); };
new Editor($markdown("text-input"), $markdown("preview"));
 </script>
