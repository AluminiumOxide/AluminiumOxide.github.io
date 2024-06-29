### 引入 Mermaid

在 head中加入 css:

```
<link rel="stylesheet" href="//unpkg.com/mermaid/dist/mermaid.min.css" />
```

在 底部 引用 js:

```
<script type="text/javascript" src="//unpkg.com/mermaid/dist/mermaid.min.js"></script>
```

### 配置文件修改

```json
window.$docsify = {
  // ...
  plugins: [
    function (hook, vm) {
      hook.ready(function () {
        mermaid.initialize({ startOnLoad: false });
      });
      hook.doneEach(function () {
        mermaid.init(undefined, '.mermaid');
      });
    }
  ],
  markdown: {
    renderer: {
      code: function (code, lang) {
        var html = '';
        if (code.match(/^sequenceDiagram/) || code.match(/^graph/) || code.match(/^gantt/)) {
          html = '<div class="mermaid">' + code + '</div>';
        }
        var hl = Prism.highlight(code, Prism.languages[lang] || Prism.languages.markup);
        return html + '<pre v-pre data-lang="' + lang + '"><code class="lang-' + lang + '">' + hl + '</code></pre>';
      }
    }
  }
};
```

### markdown 代码解析器

```json
markdown: {
  renderer: {
    code: function(code, lang) {
    var html = '';
    // 搜索 mermaid 代码
    if(code.match(/^sequenceDiagram/) || code.match(/^graph/) || code.match(/^gantt/)){
      // 生成一个 mermaid 图表的容器
      html = '<div class="mermaid">' + code + '</div>';
    }
    // 源码自带的 Prism 高亮插件
    var hl = Prism.highlight(code, Prism.languages[lang] || Prism.languages.markup)
    // 将图表的容器添加到代码之前
    return html + '<pre v-pre data-lang="' + lang + '"><code class="lang-' + lang + '">' + hl + '</code></pre>'
    }
  }
}
```

