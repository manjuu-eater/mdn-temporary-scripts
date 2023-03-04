# {{HTMLRefTable}}マクロの廃止への対応：ベタ書きテーブルに変換 #11993
# https://github.com/mdn/translated-content/pull/11993
# の Issue を出したときに使った使い捨てスクリプト
# 可読性はゼロ
# ポイするのはなんかもったいないけど保存しとくほどでもないので適当に保管しとくだけのやつ

# %%
import requests
import re
import time
from pprint import pprint
import markdown
import bs4

md=markdown.Markdown()

# %%
tdls=[
  "`<html>`",
  "`<base>`",
  "`<head>`",
  "`<link>`",
  "`<meta>`",
  "`<style>`",
  "`<title>`",
  "`<body>`",
  "`<address>`",
  "`<article>`",
  "`<aside>`",
  "`<footer>`",
  "`<header>`",
  "`<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`",
  "`<main>`",
  "`<nav>`",
  "`<section>`",
  "`<blockquote>`",
  "`<dd>`",
  "`<div>`",
  "`<dl>`",
  "`<dt>`",
  "`<figcaption>`",
  "`<figure>`",
  "`<hr>`",
  "`<li>`",
  "`<menu>`",
  "`<ol>`",
  "`<p>`",
  "`<pre>`",
  "`<ul>`",
  "`<a>`",
  "`<abbr>`",
  "`<b>`",
  "`<bdi>`",
  "`<bdo>`",
  "`<br>`",
  "`<cite>`",
  "`<code>`",
  "`<data>`",
  "`<dfn>`",
  "`<em>`",
  "`<i>`",
  "`<kbd>`",
  "`<mark>`",
  "`<q>`",
  "`<rp>`",
  "`<rt>`",
  "`<ruby>`",
  "`<s>`",
  "`<samp>`",
  "`<small>`",
  "`<span>`",
  "`<strong>`",
  "`<sub>`",
  "`<sup>`",
  "`<time>`",
  "`<u>`",
  "`<var>`",
  "`<wbr>`",
  "`<area>`",
  "`<audio>`",
  "`<img>`",
  "`<map>`",
  "`<track>`",
  "`<video>`",
  "`<embed>`",
  "`<iframe>`",
  "`<object>`",
  "`<picture>`",
  "`<portal>`",
  "`<source>`",
  "`<svg>`",
  "`<math>`",
  "`<canvas>`",
  "`<noscript>`",
  "`<script>`",
  "`<del>`",
  "`<ins>`",
  "`<caption>`",
  "`<col>`",
  "`<colgroup>`",
  "`<table>`",
  "`<tbody>`",
  "`<td>`",
  "`<tfoot>`",
  "`<th>`",
  "`<thead>`",
  "`<tr>`",
  "`<button>`",
  "`<datalist>`",
  "`<fieldset>`",
  "`<form>`",
  "`<input>`",
  "`<label>`",
  "`<legend>`",
  "`<meter>`",
  "`<optgroup>`",
  "`<option>`",
  "`<output>`",
  "`<progress>`",
  "`<select>`",
  "`<textarea>`",
  "`<details>`",
  "`<dialog>`",
  "`<summary>`",
  "`<slot>`",
  "`<template>`",
  "`<acronym>`",
  "`<applet>`",
  "`<bgsound>`",
  "`<big>`",
  "`<blink>`",
  "`<center>`",
  "`<content>`",
  "`<dir>`",
  "`<font>`",
  "`<frame>`",
  "`<frameset>`",
  "`<hgroup>`",
  "`<image>`",
  "`<keygen>`",
  "`<marquee>`",
  "`<menuitem>`",
  "`<nobr>`",
  "`<noembed>`",
  "`<noframes>`",
  "`<param>`",
  "`<plaintext>`",
  "`<rb>`",
  "`<rtc>`",
  "`<shadow>`",
  "`<spacer>`",
  "`<strike>`",
  "`<tt>`",
  "`<xmp>`"
]

# %%
innertexts=[
  "HTML の <html> 要素は HTML 文書においてルート (基点) となる要素 (トップレベル要素) であり、ルート要素とも呼ばれます。他のすべての要素は、この要素の子孫として配置しなければなりません。",
  "<base> は HTML の要素で、文書内におけるすべての相対 URL の基点となる URL を指定します。 <base> 要素は、文書内に 1 つだけ置くことができます。",
  "HTML の <head> 要素は、文書に関する機械可読な情報 (metadata)、たとえば題名、スクリプト、スタイルシートなどを含みます。",
  "HTML 外部リソースへのリンク要素 (<link>) は、現在の文書と外部のリソースとの関係を指定します。この要素はCSSへのリンクに最もよく使用されますが、サイトのアイコン (\"favicon\" スタイルのアイコンと、モバイル端末のホーム画面やアプリのアイコンの両方) の確立や、その他のことにも使用されます。",
  "HTML の <meta> 要素は、他のメタ関連要素 (base, link, script, style, title) で表すことができない任意のMetadataを提示します。",
  "HTML の <style> 要素は、文書あるいは文書の一部分のスタイル情報を含みます。",
  "<title> は HTML の要素で、Browserのタイトルバーやページのタブに表示される文書の題名を定義します。テキストのみを含めることができます。要素内のタグはすべて無視されます。",
  "HTML の <body> 要素は、 HTML 文書のコンテンツを示す要素です。 <body> 要素は文書中に一つだけ配置できます。",
  "HTML の <address> 要素は、これを含んでいる HTML が個人、団体、組織の連絡先を提供していることを示します。",
  "HTML の <article> 要素は文書、ページ、アプリケーション、サイトなどの中で自己完結しており、 (集合したものの中で) 個別に配信や再利用を行うことを意図した構成物を表します。",
  "HTML の <aside> 要素は、文書のメインコンテンツと間接的な関係しか持っていない文書の部分を表現します。",
  "HTML の <footer> 要素は、直近の区分コンテンツまたは区分化ルート要素のフッターを表します。フッターには通常、そのセクションの著作者に関する情報、関連文書へのリンク、著作権情報等を含めます。",
  "HTML の <header> 要素は、導入的なコンテンツ、ふつうは導入部やナビゲーション等のグループを表します。見出し要素だけでなく、ロゴ、検索フォーム、作者名、その他の要素を含むこともできます。",
  "HTML の <h1>–<h6> 要素は、セクションの見出しを 6 段階で表します。<h1> が最上位で、<h6> が最下位です。",
  "HTML の <main> 要素は、文書の body の主要な内容を表します。主要な内容とは、文書の中心的な主題、またはアプリケーションの中心的な機能に直接関連または拡張した内容の範囲のことです。",
  "HTML の <nav> 要素は、現在の文書内の他の部分や他の文書へのナビゲーションリンクを提供するためのセクションを表します。ナビゲーションセクションの一般的な例としてメニュー、目次、索引などがあります。",
  "HTML の <section> 要素は、文書の自立した一般的なセクション (区間) を表します。そのセクションを表現するより意味的に具体的な要素がない場合に使用します。",
  "HTML の <blockquote> 要素 (HTML ブロック引用要素) は、内包する要素の文字列が引用文であることを示します。通常、字下げを伴ってレンダリングされます (整形方法については注意の項を参照してください)。 cite 属性により引用元の文書の URL を、 cite 要素により引用元の文書のタイトルなどを明示可能です。",
  "<dd> は HTML の要素で、説明リスト要素 (dl) 内で、その前の用語 (dt) の説明、定義、値などを示します。",
  "HTML の コンテンツ区分要素 (<div>) は、フローコンテンツの汎用コンテナーです。 CSS を用いて何らかのスタイル付けがされる (例えば、スタイルが直接適用されたり、親要素にフレックスボックスなどの何らかのレイアウトモデルが適用されるなど) までは、コンテンツやレイアウトには影響を与えません。",
  "<dl> は HTML の要素で、説明リストを表します。この要素は、一連の用語（dt 要素を使用して指定）と説明（dd 要素によって提供）をリスト化したものです。一般的な使用例として、用語集の作成やメタデータ（キーと値のペアのリスト）の表示が挙げられます。",
  "<dt> は HTML の要素で、説明または定義リストの中で用語を表す部分であり、 dl の子要素としてのみ用いることができます。普通は dd 要素が続きます。しかし、複数の <dt> 要素が続くと、複数の用語がすぐ後に続く dd 要素で定義されていることを表します。",
  "HTML の <figcaption> 要素または図キャプション要素は、親の figure 要素内にあるその他のコンテンツを説明するキャプションや凡例を表します。",
  "HTML の <figure> (キャプションが付けられる図) 要素は、図表などの自己完結型のコンテンツを表し、任意で figcaption 要素を使用して表されるキャプションを付けることができます。",
  "HTML の <hr> 要素は、段落レベルの要素間において、テーマの意味的な区切りを表します。例えば、話の場面の切り替えや、節内での話題の転換などです。",
  "HTML の <li> 要素は、リストの項目を表すために用いられます。",
  "HTML の <menu> 要素は、ユーザーが実行またはアクティブ化できるコマンドのグループを表します。これは画面の上部に現れるリストメニューと、ボタンを押したときにその下部付近に現れるようなコンテキストメニューの両方を含みます。",
  "<ol> は HTML の要素で、項目の順序付きリストを表します。ふつうは番号付きのリストとして表示されます。",
  "HTML の <p> 要素は、テキストの段落を表します。",
  "<pre> は HTML の要素で、整形済みテキスト (preformatted text) を表します。この要素内のテキストは一般的に、ファイル内でのレイアウトをそのまま反映して等幅フォントで表示されます。この要素内のホワイトスペース文字はそのまま表示します。",
  "HTML の <ul> 要素は、項目の順序なしリストを表します。一般的に、行頭記号を伴うリストとして描画されます。",
  "<a> は HTML の要素（アンカー要素）で、 href 属性を用いて、別のウェブページ、ファイル、メールアドレス、同一ページ内の場所、または他の URL へのハイパーリンクを作成します。",
  "HTML の略語要素 (<abbr>) は略語や頭字語を表します。任意で title 属性で、略語の完全形または説明を提供することができます。",
  "HTML の注目付け要素 (<b>) は、要素の内容に読み手の注意を惹きたい場合で、他の特別な重要性が与えられないものに使用します。",
  "HTML の書字方向分離要素 (<bdi>) は、ブラウザーの書字方向アルゴリズムにこのテキストが周囲のテキストから独立していると扱うよう指示します。",
  "<bdo> は HTML の要素で、現在のテキストの書字方向を上書きし、中のテキストが異なる書字方向で描画されるようにします。",
  "HTML の <br> 要素 は、文中に改行（キャリッジリターン）を生成します。詩や住所など、行の分割が重要な場合に有用です。",
  "HTML の引用元要素 (<cite>) は、引用された創作物の参照を表し、作品のタイトルを含む必要があります。参照は、引用メタデータに関する利用場面に合わせた慣習に応じて省略形が用いられることがあります。",
  "HTML の <code> 要素は、コンピューターコードの短い断片の文字列であると識別できるような外見のコンテンツを表示します。",
  "HTML の <data> 要素は、与えられたコンテンツの断片を機械可読な翻訳にリンクします。コンテンツが時刻または日付に関連するものであれば、 time 要素を使用する必要があります。",
  "HTML の定義要素 (<dfn>) は、定義句や文の文脈の中で定義している用語を示すために用いられます。",
  "HTML の <em> 要素は、強調されたテキストを示します。<em> 要素は入れ子にすることができ、入れ子の段階に応じてより強い程度の強調を表すことができます。",
  "<i> は HTML の要素で、何らかの理由で他のテキストと区別されるテキストの範囲を表します。例えば、慣用句、技術用語、分類学上の呼称、などです。英文においてはよくイタリック体で表現されてきたものであり、それがこの要素の <i> という名前の元になっています。",
  "HTML のキーボード入力要素 (<kbd>) はキーボード、音声入力、その他の入力端末からのユーザーによる文字入力を表す行内の文字列の区間を表します。",
  "HTML の文字列マーク要素 (<mark>) は、周囲の文脈の中でマークを付けた部分の関連性や重要性のために、参照や記述の目的で目立たせたり強調したりする文字列を表します。",
  "HTML の <q> 要素 は、その内容が行内の引用であることを表します。最近の多くのブラウザーでは、文字列を引用符で囲むように実装しています。",
  "HTML のルビ代替表示用括弧 (<rp>) 要素は、 ruby 要素によるルビの表示に対応していないブラウザー向けの代替表示用括弧を提供するために使用します。",
  "HTML のルビ文字列 (<rt>) 要素は、ルビによる注釈（振り仮名）のルビ文字列の部分を定義し、東アジアの組版において発音、翻訳、音写などの情報を提供するために使用します。 <rt> 要素は常に ruby 要素の中で使用されます。",
  "The HTML <ruby> element はベーステキストの上、下、隣に描画される小さな注釈で、よく東アジアの文字の発音を表すのに使われます。他の種類の注釈にも使われることがありますが、この使い方はあまり一般的ではありません。",
  "HTML の <s> 要素は取り消し線を引いた文字列を表示します。 <s> 要素はすでに適切または正確ではなくなった事柄を表現します。しかし、文書の修正を示す場合、 <s> 要素は適切ではありません。この場合は del と ins の方が適しているので、こちらを使用してください。",
  "HTML のサンプル要素 (<samp>) は、コンピュータープログラムからのサンプル出力を表す行内文字列を含めるために使用されます。",
  "HTML の <small> 要素は、表示上のスタイルとは関係なく、著作権表示や法的表記のような、注釈や小さく表示される文を表します。既定では、 small から x-small のように、一段階小さいフォントでテキストが表示されます。",
  "HTML の <span> 要素は、記述コンテンツの汎用的な行内コンテナーであり、何かを表すものではありません。スタイル付けのため (class または id 属性を使用して)、または lang のような属性値を共有したりするために要素をグループ化する用途で使用することができます。",
  "HTML の強い重要性要素 (<strong>) は、内容の重要性、重大性、または緊急性が高いテキストを表します。ブラウザーは一般的に太字で描画します。",
  "HTML の 下付き文字要素 (<sub>) は、表記上の理由で下付き文字として表示するべき行内文字列を指定します。",
  "HTML の 上付き文字要素 (<sup>) は、表記上の理由で上付き文字として表示するべき行内文字列を指定します。",
  "HTML の <time> 要素は、特定の時の区間を表します。",
  "HTML の非言語的注釈要素 (<u>) は、非言語的に注釈があることを示す方法で表示する行内テキストの区間を示します。",
  "HTML の変数要素 (<var>) は、数式やプログラムコード内の変数の名前を表します。",
  "HTML の <wbr> 要素は、改行可能位置 — テキスト内でブラウザーが任意で改行してよい位置を表しますが、この改行規則は必要のない場合は改行を行いません。",
  "HTML の <area> 要素は、イメージマップの中でクリック可能な領域をあらかじめ定義します。イメージマップでは、画像上の幾何学的な領域をHyperlinkと関連付けすることができます。",
  "HTML の <audio> 要素は、文書内に音声コンテンツを埋め込むために使用します。この要素は、1つまたは複数の音源を含むことができます。音源は src 属性または source 要素を使用して表し、ブラウザーがもっとも適切な音源を選択します。また、 MediaStream を使用してストリーミングメディアを指し示すこともできます。",
  "<img> は HTML の要素で、文書に画像を埋め込みます。",
  "HTML の <map> 要素はイメージマップ (クリック可能なリンク領域) を定義するために area 要素とともに使用します。",
  "HTML の <track> 要素はメディア要素 (audio および video) の子として使用します。この要素は自動的に処理される字幕など、時間指定されたテキストトラック (または時系列データ) を指定することができます。",
  "<video> は HTML の要素で、文書中に動画再生に対応するメディアプレイヤーを埋め込みます。 <video> を音声コンテンツのために使用することもできますが、 audio 要素の方がユーザーにとって使い勝手が良いかもしれません。",
  "HTML の <embed> 要素は、外部のコンテンツを文書中の指定された場所に埋め込みます。コンテンツは外部アプリケーションや、対話型コンテンツの他の出所 (ブラウザーのプラグインなど) によって提供されます。",
  "HTML のインラインフレーム要素 (<iframe>) は、入れ子になったbrowsing contextを表現し、現在の HTML ページに他のページを埋め込むことができます。",
  "<object> は HTML の要素で、画像、内部の閲覧コンテキスト、プラグインによって扱われるリソースなどのように扱われる外部リソースを表します。",
  "HTML の <picture> 要素は、0個以上の source 要素と一つの img 要素を含み、様々な画面や端末の条件に応じた画像を提供します。",
  "HTML のポータル要素 (<portal>) は、他の HTML ページを現在のページに埋め込み、新しいページへの移動がスムーズにできるようにします。",
  "HTML の <source> 要素は、 picture 要素、 audio 要素、 video 要素に対し、複数のメディアリソースを指定します。",
  "svg 要素は、新しい座標系とビューポートを定義するコンテナーです。これは SVG 文書の最も外側の要素として使用されますが、SVG または HTML 文書の中に SVG フラグメントを埋め込むためにも使用できます。",
  "MathML における最上位の要素は <math> です。有効な MathML のインスタンスはすべて <math> タグに囲まれています。加えて、 <math> 要素を入れ子状に配置してはなりませんが、中にその他の子要素をいくつでも持つことができます。",
  "HTML の <canvas> 要素 と Canvas スクリプティング API や WebGL API を使用して、グラフィックやアニメーションを描画することができます。",
  "HTML の <noscript> 要素は、このページ上のスクリプトの種類に対応していない場合や、スクリプトの実行がブラウザーで無効にされている場合に表示する HTML の部分を定義します。",
  "<script> は HTML の要素で、実行できるコードやデータを埋め込むために使用します。ふつうは JavaScript のコードの埋め込みや参照に使用されます。 <script> 要素は WebGL の GLSL shader プログラミング言語、 JSON 等の他の言語にも使用することができます。",
  "HTML の <del> 要素は、文書から削除された文字列の範囲を表します。",
  "HTML の <ins> 要素",
  "HTML の <caption> 要素は、表のキャプション (またはタイトル) を指定します。",
  "HTML の <col> 要素は、表内の列を定義して、すべての一般セルに共通の意味を定義するために使用します。この要素は通常、 colgroup 要素内にみられます。",
  "HTML の <colgroup> 要素は、表内の列のグループを定義します。",
  "HTML の <table> 要素は表形式のデータ、つまり、行と列の組み合わせによるセルに含まれたデータによる二次元の表で表現される情報です。",
  "HTML の表本体要素 (<tbody>) は、表の一連の行 (tr 要素) を内包し、その部分が表 (table) の本体部分を構成することを表します。",
  "HTML の <td> 要素は、表でデータを包含するセルを定義します。これは表モデルに関与します。",
  "<tfoot> は HTML の要素で、表の一連の列を総括する行のセットを定義します。",
  "HTML の <th> 要素は、表のセルのグループ用のヘッダーであるセルを定義します。このグループの性質は、scope 属性と headers 属性で定義します。",
  "<thead> は HTML の要素で、表の列の見出しを定義する行のセットを定義します。",
  "HTML の <tr> 要素は、表内でセルの行を定義します。行のセルは td (データセル) および th (見出しセル) 要素をを混在させることができます。",
  "HTML の <button> 要素はクリックできるボタンを表し、フォームや、文書で単純なボタン機能が必要なあらゆる場所で使用することができます。",
  "HTML の <datalist> 要素は、他のコントロールで利用可能な値を表現する一連の option 要素を含みます。",
  "HTML の <fieldset> 要素は、ウェブフォーム内のラベル (label) などのようにいくつかのコントロールをグループ化するために使用します。",
  "<form> は HTML の要素で、ウェブサーバーに情報を送信するための対話型コントロールを含む文書の区間を表します。",
  "<input> は HTML の要素で、ユーザーからデータを受け取るための、ウェブベースのフォーム用の対話的なコントロールを作成するために使用します。端末とuser agentによりますが、広範に渡る種類のデータ入力やコントロールウィジェットが利用できます。 <input> 要素は入力型と属性の組み合わせの数が非常に多いため、 HTML の中で最も強力かつ最も複雑な要素の一つです。",
  "HTML の <label> 要素は、ユーザーインターフェイスの項目のキャプションを表します。",
  "HTML の <legend> 要素は、その親要素である fieldset の内容のキャプションを表します。",
  "HTML の <meter> 要素は、既知の範囲内のスカラー値、または小数値を表します。",
  "<optgroup> は HTML の要素で、 select 要素内の選択肢 (option) のグループを作成します。",
  "HTML の <option> 要素は、 select 要素、optgroup 要素、datalist 要素内で項目を定義するために使われます。したがって、<option> は HTML 文書でポップアップメニューのメニュー項目や、その他の項目の一覧を表すことができます。",
  "HTML の出力要素 (<output>) は、サイトやアプリが計算結果やユーザー操作の結果を挿入することができるコンテナー要素です。",
  "HTML の <progress> 要素は、タスクの進捗状況を表示します。プログレスバーとしてよく表示されます。",
  "HTML の <select> 要素は、選択式のメニューを提供するコントロールを表します。",
  "HTML の <textarea> 要素は、複数行のプレーンテキスト編集コントロールを表し、レビューのコメントやお問い合わせフォーム等のように、ユーザーが大量の自由記述テキストを入力できるようにするときに便利です。",
  "HTML の詳細折りたたみ要素 (<details>) は、ウィジェットが「開いた」状態になった時のみ情報が表示される折りたたみウィジェットを作成します。",
  "HTML の <dialog> 要素は、ダイアログボックスや、消すことができるアラート、インスペクター、サブウィンドウ等のような対話的コンポーネントを表します。",
  "HTML の概要明示要素 (<summary>) は、 details 要素の内容の要約、キャプション、説明、凡例を表します。",
  "<slot> は HTML の要素 — ウェブコンポーネント技術の一部 — は、ウェブコンポーネント内で別な DOM ツリーを構築し、いっしょに表示することができる独自のマークアップを入れることができるプレイスホルダーです。",
  "<template> は HTML の要素で、ページが読み込まれたときにすぐにレンダリングされるのではなく、実行時に JavaScript を使って後からインスタンス化することができる HTML を保持するためのメカニズムです。",
  "<acronym> は HTML の要素で、頭字語または略語の単語を構成する文字の並びを明示することができます。",
  "HTML の アプレット要素 (<applet>) は文書に Java アプレットを埋め込みます。この要素は object にとって代わり、廃止されました。",
  "<bgsound> は HTML の非推奨の要素です。そのページが使用されている間の背景として再生される音声ファイルを設定します。代わりに audio 要素を使用してください。",
  "<big> は HTML の非推奨の要素で、内包するテキストを周りの文字列よりも1段階大きいフォントの大きさで描画します（例えば medium が large になります）。大きさはブラウザーの最大フォントの大きさに制限されます。",
  "<blink> は HTML の要素で、標準外の要素であり、包含するテキストをゆっくり点滅させます。",
  "<center> は HTML の要素で、中に含まれるブロックレベルまたはインラインコンテンツを中央揃えして表示するブロックレベル要素です。コンテナーはふつう body ですが、必ずしもそうとは限りません。",
  "HTML の <content> 要素は、一連のウェブコンポーネント技術の廃止された部分であり、 Shadow DOM (en-US) の中で insertion point として使われていましたが、通常の HTML で利用することは意図されていませんでした。",
  "<dir> は HTML の要素で、user agentが適用するスタイルやアイコンを用いて表示する、ファイルやフォルダーのディレクトリーのコンテナとして使われます。この要素は廃止されたので使わないで下さい。代わりに、ファイル一覧を含め、一覧には ul 要素を使用してください。",
  "<font> は HTML の要素で、その内容のフォントサイズ、文字色、使用フォントを定義します。",
  "<frame> は、別の HTML 文書を表示できる個々の領域を定義する HTML 要素です。 frame 要素は frameset の内部で使用します。",
  "HTML の <frameset> 要素は、 frame 要素を包含するために使用する HTML 要素です。",
  "HTML の <hgroup> 要素は、文書のセクションの、複数レベルの見出しを表します。これは <h1>–<h6> 要素のセットをグループ化します。",
  "<image> は HTML の要素で、 img 要素の古く、対応が不十分な前身です。 使用しないでください。",
  "<keygen> は HTML の要素で、鍵の材料の生成を容易にするため、および HTML フォームの一部として公開鍵を送信するための要素です。この仕組みは、ウェブベースの資格情報管理システムと合わせて使用するものとして設計されています。証明書の要求に必要な他の情報を伴う HTML フォームで <keygen> 要素を使用して、その処理結果が署名済み資格情報になることを想定しています。",
  "<marquee> は HTML の要素で、テキストがスクロールする領域を挿入します。要素の属性を使用して、テキストがコンテンツ領域の端に達したときにどうするかを制御できます。",
  "HTML の <menuitem> 要素は、ユーザーがポップアップメニューから実行できるコマンドをあらわします。メニューボタンに割り当てるメニューはもちろん、コンテキストメニューも含みます。",
  "<nobr> は HTML の要素で、その内包する文字列の自動改行を無効化します。行内に収まらない文字列は、領域からはみ出てレンダリングされるか、スクロールバーを伴って表示されます。",
  "<noembed> は HTML の要素で、廃止された、標準外の方法であり、 embed 要素に対応していないブラウザーや、ユーザーが仕様とした種類の埋め込みコンテンツに対応していないブラウザーで代替または「フォールバック」コンテンツを提供するものです。これは HTML 4.01 で非推奨となり、代替コンテンツは object 要素の開始タグと終了タグの間に配置されるようになりました。",
  "<noframes> は HTML の要素で、 frame 要素に対応していない（または対応を無効化した）ブラウザーのためのコンテンツを提供します。よく使われるほとんどのブラウザーがフレームに対応していますが、一部のモバイルブラウザーやテキストモードブラウザーなどの例外もあります。",
  "HTML の <param> 要素は、object 要素の引数を定義します。",
  "<plaintext> は HTML の要素で、開始タグ以降のすべてを生のテキストとして表示し、それ以降の HTML を無視します。開始タグ以降は全て生のテキスト扱いになるので、終了タグはありません。",
  "HTML ルビベース (<rb>) 要素は、 ruby 表記のベースとなるテキストの部分を区切るために使用されます。つまり、修飾される文字列です。",
  "HTML のルビ文字列コンテナー (<rtc>) 要素は、 ruby 要素内で使用する rb 要素にルビで与える文字列の、意味を表す注釈を包含します。rb 要素は発音の注釈 (rt) と意味の注釈 (rtc) の両方を持つことができます。",
  "HTML <shadow> 要素 (Web Components 技術スイートの廃止された部分) は shadow DOM の insertion point として使用するものでした。",
  "<spacer> は HTML の要素で、ウェブページに空の空間を挿入するための廃止された HTML 要素です。ウェブデザイナーによって用いられていた 1px の透過 GIF 画像（いわゆるスペーサー GIF）の挿入と同様の効果を実現するために Netscape 社が実装したものです。しかし <spacer> はほとんどの主要ブラウザーで対応されず、また、同様の効果は CSS を用いて実現可能です。",
  "<strike> は HTML の要素で、テキストの上に取り消し線（水平線）を引きます。",
  "<tt> は HTML は、user agentの既定の等幅フォントで表示される行内文字列を生成します。この要素は、テレタイプ、テキスト専用画面、ラインプリンターのような等幅の表示装置で表示されるテキストとしてスタイルを設定しようとするものです。",
  "<xmp> は HTML の要素で、その開始タグから終了タグまでの間のタグを HTML として解釈せず、等幅フォントでレンダリングします。 HTML2 仕様書では、これを 1 行当たり 80 文字を表示するのに充分な幅でレンダリングするよう推奨しています。"
]

# %%
rawurls=[
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/html/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/base/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/head/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/link/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/meta/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/style/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/title/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/body/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/address/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/article/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/aside/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/footer/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/header/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/heading_elements/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/main/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/nav/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/section/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/blockquote/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dd/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/div/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dl/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dt/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/figcaption/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/figure/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/hr/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/li/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/menu/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/ol/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/p/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/pre/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/ul/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/a/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/abbr/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/b/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/bdi/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/bdo/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/br/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/cite/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/code/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/data/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dfn/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/em/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/i/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/kbd/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/mark/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/q/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/rp/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/rt/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/ruby/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/s/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/samp/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/small/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/span/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/strong/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/sub/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/sup/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/time/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/u/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/var/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/wbr/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/area/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/audio/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/img/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/map/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/track/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/video/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/embed/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/iframe/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/object/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/picture/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/portal/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/source/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/svg/element/svg/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/mathml/element/math/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/canvas/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/noscript/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/script/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/del/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/ins/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/caption/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/col/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/colgroup/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/table/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/tbody/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/td/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/tfoot/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/th/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/thead/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/tr/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/button/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/datalist/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/fieldset/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/form/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/input/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/label/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/legend/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/meter/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/optgroup/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/option/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/output/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/progress/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/select/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/textarea/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/details/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dialog/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/summary/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/slot/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/template/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/acronym/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/applet/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/bgsound/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/big/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/blink/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/center/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/content/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/dir/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/font/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/frame/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/frameset/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/hgroup/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/image/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/keygen/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/marquee/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/menuitem/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/nobr/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/noembed/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/noframes/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/param/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/plaintext/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/rb/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/rtc/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/shadow/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/spacer/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/strike/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/tt/index.md",
  "https://raw.githubusercontent.com/mdn/translated-content/main/files/ja/web/html/element/xmp/index.md"
]

# %%
section_tag_lists=[
    ["html",], 
    ["base","head","link","meta","style","title",], 
    ["body",], 
    ["address","article","aside","footer","header","h1","main","nav","section",], 
    ["blockquote","dd","div","dl","dt","figcaption","figure","hr","li","menu","ol","p","pre","ul",], 
    ["a","abbr","b","bdi","bdo","br","cite","code","data","dfn","em","i","kbd","mark","q","rp","rt","ruby","s","samp","small","span","strong","sub","sup","time","u","var","wbr",], 
    ["area","audio","img","map","track","video",], 
    ["embed","iframe","object","picture","portal","source",], 
    ["svg","math",], 
    ["canvas","noscript","script",], 
    ["del","ins",], 
    ["caption","col","colgroup","table","tbody","td","tfoot","th","thead","tr",], 
    ["button","datalist","fieldset","form","input","label","legend","meter","optgroup","option","output","progress","select","textarea",], 
    ["details","dialog","summary",], 
    ["slot","template",], 
    ["acronym","applet","bgsound","big","blink","center","content","dir","font","frame","frameset","image","keygen","marquee","menuitem","nobr","noembed","noframes","param","plaintext","rb","rtc","shadow","spacer","strike","tt","xmp"],
]

# %%
def get_content(url):
    res = requests.get(url)
    time.sleep(0.5)
    return res.text
    
def get_contents(urls):
    return [get_content(url) for url in urls]

# %%
def getsummary(text):
    if not text:return ""

    splited=text.splitlines()
    count=0
    for i, line in enumerate(splited):
        if re.search(r"^-+$", line):
            count+=1
        if count>1:break
    else:
        raise Exception(text[:100])
    splited=splited[i+1:]

    for i, line in enumerate(splited):
        if (
                re.search(r"^\s*$", line)
                or re.search(r"^(\{\{[^}]*\}\}\s*)*$", line)
                or re.search(r"^#+", line)
                or re.search(r"^-+ ", line)
                ):
            continue
        remove_str = "  - : "
        if line.startswith(remove_str):
            line = line.replace(remove_str, "", 1)
        return line
    else:
        raise Exception(text[:100])
    raise


# %%
def htmltoinnertext(text):
    b=bs4.BeautifulSoup(text)
    return b.text

# %%
def rawurltootherlocale(rawurl, locale):
    prefix="https://raw.githubusercontent.com/mdn/translated-content/main/files/"
    jalocale="ja"
    beforeurll=prefix+jalocale+"/"

    if not beforeurll in rawurl:raise
    afterurll=prefix+locale+"/"
    return rawurl.replace(beforeurll, afterurll)

def rawurlstootherlocale(rawurls, locale):
    return [rawurltootherlocale(rawurl, locale) for rawurl in rawurls]

# %%
locales = ["ja","es","fr","ko","pt-BR","ru","zh-CN","zh-TW",]
rawurls_localedict={
    locale: rawurlstootherlocale(rawurls, locale.lower())
    for locale in locales
}

# %%
"""sources_localedict={
    locale: get_contents(rawurls_localedict[locale])
    for locale in locales
}"""

# %%
def rawurl_to_enus(rawurl):
    prefix="https://raw.githubusercontent.com/mdn/translated-content/main/files/"
    jalocale="ja"
    beforeurll=prefix+jalocale+"/"

    #             https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/html/element/html/index.md
    after_prefix="https://raw.githubusercontent.com/mdn/content/main/files/"
    if not beforeurll in rawurl:raise
    locale="en-us"
    afterurll=after_prefix+locale+"/"
    return rawurl.replace(beforeurll, afterurll)

def rawurls_to_enus(rawurls):
    return [rawurl_to_enus(rawurl) for rawurl in rawurls]
    
#enus_sources=get_contents(rawurls_to_enus(rawurls_localedict["ja"]))


# %%
def get_file_content(path):
    try:
        with open(path, encoding="utf-8") as f:
            s=f.read()
        return s
    except FileNotFoundError:
        print("FileNotFoundError: "+path)
        pass
    try:
        with open(path.lower(), encoding="utf-8") as f:
            s=f.read()
        return s
    except FileNotFoundError:
        print("FileNotFoundError: "+path.lower())
        pass
    return ""
    
def get_file_contents(paths):
    return [get_file_content(path) for path in paths]
    
def url_to_filepath(url):
    prefix="https://raw.githubusercontent.com/mdn/translated-content/main/"
    return url.replace(prefix, "")

def get_file_contents_with_urls(urls):
    return get_file_contents([url_to_filepath(url) for url in urls])

# %%
sources_f_localedict={
    locale.lower(): get_file_contents_with_urls(rawurls_localedict[locale])
    for locale in locales
}

# %%
summaries_f_localedict={
    locale: [getsummary(src) for src in srcs]
    for locale, srcs in sources_f_localedict.items()
}

# %%
#enus_summaries=[getsummary(src) for src in enus_sources]
enus_summaries="""\
Represents the root (top-level element) of an HTML document, so it is also referred to as the _root element_. All other elements must be descendants of this element.
Specifies the base URL to use for all relative URLs in a document. There can be only one such element in a document.
Contains machine-readable information (metadata) about the document, like its [title](/en-US/docs/Web/HTML/Element/title), [scripts](/en-US/docs/Web/HTML/Element/script), and [style sheets](/en-US/docs/Web/HTML/Element/style).
Specifies relationships between the current document and an external resource. This element is most commonly used to link to CSS, but is also used to establish site icons (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.
Represents {{Glossary("Metadata","metadata")}} that cannot be represented by other HTML meta-related elements, like {{HTMLElement("base")}}, {{HTMLElement("link")}}, {{HTMLElement("script")}}, {{HTMLElement("style")}} and {{HTMLElement("title")}}.
Contains style information for a document, or part of a document. It contains CSS, which is applied to the contents of the document containing this element.
Defines the document's title that is shown in a {{glossary("Browser", "browser")}}'s title bar or a page's tab. It only contains text; tags within the element are ignored.
represents the content of an HTML document. There can be only one such element in a document.
Indicates that the enclosed HTML provides contact information for a person or people, or for an organization.
Represents a self-contained composition in a document, page, application, or site, which is intended to be independently distributable or reusable (e.g., in syndication). Examples include: a forum post, a magazine or newspaper article, or a blog entry, a product card, a user-submitted comment, an interactive widget or gadget, or any other independent item of content.
Represents a portion of a document whose content is only indirectly related to the document's main content. Asides are frequently presented as sidebars or call-out boxes.
Represents a footer for its nearest ancestor [sectioning content](/en-US/docs/Web/HTML/Content_categories#sectioning_content) or [sectioning root](/en-US/docs/Web/HTML/Element/Heading_Elements) element. A `<footer>` typically contains information about the author of the section, copyright data or links to related documents.
Represents introductory content, typically a group of introductory or navigational aids. It may contain some heading elements but also a logo, a search form, an author name, and other elements.
Represent six levels of section headings. `<h1>` is the highest section level and `<h6>` is the lowest.
Represents the dominant content of the body of a document. The main content area consists of content that is directly related to or expands upon the central topic of a document, or the central functionality of an application.
Represents a section of a page whose purpose is to provide navigation links, either within the current document or to other documents. Common examples of navigation sections are menus, tables of contents, and indexes.
Represents a generic standalone section of a document, which doesn't have a more specific semantic element to represent it. Sections should always have a heading, with very few exceptions.
Indicates that the enclosed text is an extended quotation. Usually, this is rendered visually by indentation. A URL for the source of the quotation may be given using the `cite` attribute, while a text representation of the source can be given using the {{HTMLElement("cite")}} element.
Provides the description, definition, or value for the preceding term ({{HTMLElement("dt")}}) in a description list ({{HTMLElement("dl")}}).
The generic container for flow content. It has no effect on the content or layout until styled in some way using CSS (e.g., styling is directly applied to it, or some kind of layout model like {{glossary("Flexbox", "flexbox")}} is applied to its parent element).
Represents a description list. The element encloses a list of groups of terms (specified using the {{HTMLElement("dt")}} element) and descriptions (provided by {{HTMLElement("dd")}} elements). Common uses for this element are to implement a glossary or to display metadata (a list of key-value pairs).
Specifies a term in a description or definition list, and as such must be used inside a {{HTMLElement("dl")}} element. It is usually followed by a {{HTMLElement("dd")}} element; however, multiple `<dt>` elements in a row indicate several terms that are all defined by the immediate next {{HTMLElement("dd")}} element.
Represents a caption or legend describing the rest of the contents of its parent {{HTMLElement("figure")}} element.
Represents self-contained content, potentially with an optional caption, which is specified using the {{HTMLElement("figcaption")}} element. The figure, its caption, and its contents are referenced as a single unit.
Represents a thematic break between paragraph-level elements: for example, a change of scene in a story, or a shift of topic within a section.
Represents an item in a list. It must be contained in a parent element: an ordered list ({{HTMLElement("ol")}}), an unordered list ({{HTMLElement("ul")}}), or a menu ({{HTMLElement("menu")}}). In menus and unordered lists, list items are usually displayed using bullet points. In ordered lists, they are usually displayed with an ascending counter on the left, such as a number or letter.
A semantic alternative to ({{HTMLElement("ul")}}, but treated by browsers (and exposed through the accessibility tree) as no different than ({{HTMLElement("ul")}}. It represents an unordered list of items (which are represented by ({{HTMLElement("li")}} elements).
Represents an ordered list of items — typically rendered as a numbered list.
Represents a paragraph. Paragraphs are usually represented in visual media as blocks of text separated from adjacent blocks by blank lines and/or first-line indentation, but HTML paragraphs can be any structural grouping of related content, such as images or form fields.
Represents preformatted text which is to be presented exactly as written in the HTML file. The text is typically rendered using a non-proportional, or [monospaced](https://en.wikipedia.org/wiki/Monospaced_font), font. Whitespace inside this element is displayed as written.
Represents an unordered list of items, typically rendered as a bulleted list.
Together with its `href` attribute, creates a hyperlink to web pages, files, email addresses, locations in the same page, or anything else a URL can address.
Represents an abbreviation or acronym.
Used to draw the reader's attention to the element's contents, which are not otherwise granted special importance. This was formerly known as the Boldface element, and most browsers still draw the text in boldface. However, you should not use `<b>` for styling text or granting importance. If you wish to create boldface text, you should use the CSS {{cssxref("font-weight")}} property. If you wish to indicate an element is of special importance, you should use the strong element.
Tells the browser's bidirectional algorithm to treat the text it contains in isolation from its surrounding text. It's particularly useful when a website dynamically inserts some text and doesn't know the directionality of the text being inserted.
Overrides the current directionality of text, so that the text within is rendered in a different direction.
Produces a line break in text (carriage-return). It is useful for writing a poem or an address, where the division of lines is significant.
Used to mark up the title of a cited creative work. The reference may be in an abbreviated form according to context-appropriate conventions related to citation metadata.
Displays its contents styled in a fashion intended to indicate that the text is a short fragment of computer code. By default, the content text is displayed using the user agent default monospace font.
Links a given piece of content with a machine-readable translation. If the content is time- or date-related, the time element must be used.
Used to indicate the term being defined within the context of a definition phrase or sentence. The ancestor {{HTMLElement("p")}} element, the {{HTMLElement("dt")}}/{{HTMLElement("dd")}} pairing, or the nearest section ancestor of the `<dfn>` element, is considered to be the definition of the term.
Marks text that has stress emphasis. The `<em>` element can be nested, with each level of nesting indicating a greater degree of emphasis.
Represents a range of text that is set off from the normal text for some reason, such as idiomatic text, technical terms, taxonomical designations, among others. Historically, these have been presented using italicized type, which is the original source of the `<i>` naming of this element.
Represents a span of inline text denoting textual user input from a keyboard, voice input, or any other text entry device. By convention, the user agent defaults to rendering the contents of a `<kbd>` element using its default monospace font, although this is not mandated by the HTML standard.
Represents text which is marked or highlighted for reference or notation purposes due to the marked passage's relevance in the enclosing context.
Indicates that the enclosed text is a short inline quotation. Most modern browsers implement this by surrounding the text in quotation marks. This element is intended for short quotations that don't require paragraph breaks; for long quotations use the {{HTMLElement("blockquote")}} element.
Used to provide fall-back parentheses for browsers that do not support display of ruby annotations using the {{HTMLElement("ruby")}} element. One `<rp>` element should enclose each of the opening and closing parentheses that wrap the {{HTMLElement("rt")}} element that contains the annotation's text.
Specifies the ruby text component of a ruby annotation, which is used to provide pronunciation, translation, or transliteration information for East Asian typography. The `<rt>` element must always be contained within a {{HTMLElement("ruby")}} element.
Represents small annotations that are rendered above, below, or next to base text, usually used for showing the pronunciation of East Asian characters. It can also be used for annotating other kinds of text, but this usage is less common.
Renders text with a strikethrough, or a line through it. Use the `<s>` element to represent things that are no longer relevant or no longer accurate. However, `<s>` is not appropriate when indicating document edits; for that, use the del and ins elements, as appropriate.
Used to enclose inline text which represents sample (or quoted) output from a computer program. Its contents are typically rendered using the browser's default monospaced font (such as [Courier](<https://en.wikipedia.org/wiki/Courier_(typeface)>) or Lucida Console).
Represents side-comments and small print, like copyright and legal text, independent of its styled presentation. By default, it renders text within it one font-size smaller, such as from `small` to `x-small`.
A generic inline container for phrasing content, which does not inherently represent anything. It can be used to group elements for styling purposes (using the `class` or `id` attributes), or because they share attribute values, such as `lang`. It should be used only when no other semantic element is appropriate. `<span>` is very much like a div element, but div is a [block-level element](/en-US/docs/Web/HTML/Block-level_elements) whereas a `<span>` is an [inline element](/en-US/docs/Web/HTML/Inline_elements).
Indicates that its contents have strong importance, seriousness, or urgency. Browsers typically render the contents in bold type.
Specifies inline text which should be displayed as subscript for solely typographical reasons. Subscripts are typically rendered with a lowered baseline using smaller text.
Specifies inline text which is to be displayed as superscript for solely typographical reasons. Superscripts are usually rendered with a raised baseline using smaller text.
Represents a specific period in time. It may include the datetime attribute to translate dates into machine-readable format, allowing for better search engine results or custom features such as reminders.
Represents a span of inline text which should be rendered in a way that indicates that it has a non-textual annotation. This is rendered by default as a simple solid underline, but may be altered using CSS.
Represents the name of a variable in a mathematical expression or a programming context. It's typically presented using an italicized version of the current typeface, although that behavior is browser-dependent.
Represents a word break opportunity—a position within text where the browser may optionally break a line, though its line-breaking rules would not otherwise create a break at that location.
Defines an area inside an image map that has predefined clickable areas. An _image map_ allows geometric areas on an image to be associated with{{Glossary("Hyperlink", "hyperlink")}}.
Used to embed sound content in documents. It may contain one or more audio sources, represented using the `src` attribute or the source element: the browser will choose the most suitable one. It can also be the destination for streamed media, using a {{domxref("MediaStream")}}.
Embeds an image into the document.
Used with {{HTMLElement("area")}} elements to define an image map (a clickable link area).
Used as a child of the media elements, audio and video. It lets you specify timed text tracks (or time-based data), for example to automatically handle subtitles. The tracks are formatted in [WebVTT format](/en-US/docs/Web/API/WebVTT_API) (`.vtt` files)—Web Video Text Tracks.
Embeds a media player which supports video playback into the document. You can use `<video>` for audio content as well, but the audio element may provide a more appropriate user experience.
Embeds external content at the specified point in the document. This content is provided by an external application or other source of interactive content such as a browser plug-in.
Represents a nested browsing context, embedding another HTML page into the current one.
Represents an external resource, which can be treated as an image, a nested browsing context, or a resource to be handled by a plugin.
Contains zero or more {{HTMLElement("source")}} elements and one {{HTMLElement("img")}} element to offer alternative versions of an image for different display/device scenarios.
Enables the embedding of another HTML page into the current one for the purposes of allowing smoother navigation into new pages.
Specifies multiple media resources for the picture, the audio element, or the video element. It is a void element, meaning that it has no content and does not have a closing tag. It is commonly used to offer the same media content in multiple file formats in order to provide compatibility with a broad range of browsers given their differing support for [image file formats](/en-US/docs/Web/Media/Formats/Image_types) and [media file formats](/en-US/docs/Web/Media/Formats).
Container defining a new coordinate system and [viewport](/en-US/docs/Web/SVG/Attribute/viewBox). It is used as the outermost element of SVG documents, but it can also be used to embed an SVG fragment inside an SVG or HTML document.
The top-level element in MathML. Every valid MathML instance must be wrapped in it. In addition you must not nest a second `<math>` element in another, but you can have an arbitrary number of other child elements in it.
Container element to use with either the [canvas scripting API](/en-US/docs/Web/API/Canvas_API) or the [WebGL API](/en-US/docs/Web/API/WebGL_API) to draw graphics and animations.
Defines a section of HTML to be inserted if a script type on the page is unsupported or if scripting is currently turned off in the browser.
Used to embed executable code or data; this is typically used to embed or refer to JavaScript code. The `<script>` element can also be used with other languages, such as [WebGL](/en-US/docs/Web/API/WebGL_API)'s GLSL shader programming language and [JSON](/en-US/docs/Glossary/JSON).
Represents a range of text that has been deleted from a document. This can be used when rendering "track changes" or source code diff information, for example. The `<ins>` element can be used for the opposite purpose: to indicate text that has been added to the document.
Represents a range of text that has been added to a document. You can use the `<del>` element to similarly represent a range of text that has been deleted from the document.
Specifies the caption (or title) of a table.
Defines a column within a table and is used for defining common semantics on all common cells. It is generally found within a {{HTMLElement("colgroup")}} element.
Defines a group of columns within a table.
Represents tabular data — that is, information presented in a two-dimensional table comprised of rows and columns of cells containing data.
Encapsulates a set of table rows ({{HTMLElement("tr")}} elements), indicating that they comprise the body of the table ({{HTMLElement("table")}}).
Defines a cell of a table that contains data. It participates in the _table model_.
Defines a set of rows summarizing the columns of the table.
Defines a cell as header of a group of table cells. The exact nature of this group is defined by the `scope` and `headers` attributes.
Defines a set of rows defining the head of the columns of the table.
Defines a row of cells in a table. The row's cells can then be established using a mix of {{HTMLElement("td")}} (data cell) and {{HTMLElement("th")}} (header cell) elements.
An interactive element activated by a user with a mouse, keyboard, finger, voice command, or other assistive technology. Once activated, it then performs an action, such as submitting a [form](/en-US/docs/Learn/Forms) or opening a dialog.
Contains a set of {{HTMLElement("option")}} elements that represent the permissible or recommended options available to choose from within other controls.
Used to group several controls as well as labels ({{HTMLElement("label")}}) within a web form.
Represents a document section containing interactive controls for submitting information.
Used to create interactive controls for web-based forms in order to accept data from the user; a wide variety of types of input data and control widgets are available, depending on the device and user agent. The `<input>` element is one of the most powerful and complex in all of HTML due to the sheer number of combinations of input types and attributes.
Represents a caption for an item in a user interface.
Represents a caption for the content of its parent {{HTMLElement("fieldset")}}.
Represents either a scalar value within a known range or a fractional value.
Creates a grouping of options within a {{HTMLElement("select")}} element.
Used to define an item contained in a select, an {{HTMLElement("optgroup")}}, or a {{HTMLElement("datalist")}} element. As such, `<option>` can represent menu items in popups and other lists of items in an HTML document.
Container element into which a site or app can inject the results of a calculation or the outcome of a user action.
Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.
Represents a control that provides a menu of options.
Represents a multi-line plain-text editing control, useful when you want to allow users to enter a sizeable amount of free-form text, for example a comment on a review or feedback form.
Creates a disclosure widget in which information is visible only when the widget is toggled into an "open" state. A summary or label must be provided using the {{HTMLElement("summary")}} element.
Represents a dialog box or other interactive component, such as a dismissible alert, inspector, or subwindow.
Specifies a summary, caption, or legend for a details element's disclosure box. Clicking the `<summary>` element toggles the state of the parent {{HTMLElement("details")}} element open and closed.
Part of the [Web Components](/en-US/docs/Web/Web_Components) technology suite, this element is a placeholder inside a web component that you can fill with your own markup, which lets you create separate DOM trees and present them together.
A mechanism for holding HTML that is not to be rendered immediately when a page is loaded but may be instantiated subsequently during runtime using JavaScript.
Allows authors to clearly indicate a sequence of characters that compose an acronym or abbreviation for a word.
Embeds a Java applet into the document; this element has been deprecated in favor of {{HTMLElement("object")}}.
Sets up a sound file to play in the background while the page is used; use {{HTMLElement("audio")}} instead.
Renders the enclosed text at a font size one level larger than the surrounding text (`medium` becomes `large`, for example). The size is capped at the browser's maximum permitted font size.
Causes the enclosed text to flash slowly.
Displays its block-level or inline contents centered horizontally within its containing element.
An obsolete part of the [Web Components](/en-US/docs/Web/Web_Components) suite of technologies—was used inside of [Shadow DOM](/en-US/docs/Web/Web_Components/Using_shadow_DOM) as an insertion point, and wasn't meant to be used in ordinary HTML. It has now been replaced by the {{HTMLElement("slot")}} element, which creates a point in the DOM at which a shadow DOM can be inserted.
Container for a directory of files and/or folders, potentially with styles and icons applied by the user agent. Do not use this obsolete element; instead, you should use the {{HTMLElement("ul")}} element for lists, including lists of files.
Defines the font size, color and face for its content.
Defines a particular area in which another HTML document can be displayed. A frame should be used within a {{HTMLElement("frameset")}}.
Used to contain {{HTMLElement("frame")}} elements.
An ancient and poorly supported precursor to the {{HTMLElement("img")}} element. It should not be used.
Exists to facilitate generation of key material, and submission of the public key as part of an [HTML form](/en-US/docs/Learn/Forms). This mechanism is designed for use with Web-based certificate management systems. It is expected that the `<keygen>` element will be used in an HTML form along with other information needed to construct a certificate request, and that the result of the process will be a signed certificate.
Used to insert a scrolling area of text. You can control what happens when the text reaches the edges of its content area using its attributes.
Represents a command that a user is able to invoke through a popup menu. This includes context menus, as well as menus that might be attached to a menu button.
Prevents the text it contains from automatically wrapping across multiple lines, potentially resulting in the user having to scroll horizontally to see the entire width of the text.
An obsolete, non-standard way to provide alternative, or "fallback", content for browsers that do not support the embed element or do not support the type of [embedded content](/en-US/docs/Web/HTML/Content_categories#embedded_content) an author wishes to use. This element was deprecated in HTML 4.01 and above in favor of placing fallback content between the opening and closing tags of an {{HTMLElement("object")}} element.
Provides content to be presented in browsers that don't support (or have disabled support for) the {{HTMLElement("frame")}} element. Although most commonly-used browsers support frames, there are exceptions, including certain special-use browsers including some mobile browsers, as well as text-mode browsers.
Defines parameters for an {{HTMLElement("object")}} element.
Renders everything following the start tag as raw text, ignoring any following HTML. There is no closing tag, since everything after it is considered raw text.
Used to delimit the base text component of a ruby annotation, i.e. the text that is being annotated. One `<rb>` element should wrap each separate atomic segment of the base text.
Embraces semantic annotations of characters presented in a ruby of {{HTMLElement("rb")}} elements used inside of {{HTMLElement("ruby")}} element. {{HTMLElement("rb")}} elements can have both pronunciation ({{HTMLElement("rt")}}) and semantic ({{HTMLElement("rtc")}}) annotations.
An obsolete part of the [Web Components](/en-US/docs/Web/Web_Components) technology suite that was intended to be used as a shadow DOM insertion point. You might have used it if you have created multiple shadow roots under a shadow host.
Allows insertion of empty spaces on pages. It was devised by Netscape to accomplish the same effect as a single-pixel layout image, which was something web designers used to use to add white spaces to web pages without actually using an image. However, `<spacer>` is no longer supported by any major browser and the same effects can now be achieved using simple CSS.
Places a strikethrough (horizontal line) over text.
Creates inline text which is presented using the user agent default monospace font face. This element was created for the purpose of rendering text as it would be displayed on a fixed-width display such as a teletype, text-only screen, or line printer.
Renders text between the start and end tags without interpreting the HTML in between and using a monospaced font. The HTML2 specification recommended that it should be rendered wide enough to allow 80 characters per line.
""".splitlines()

# %%
def locale_link(link, locale):
    localed = re.sub(r"^/[^/]+/", rf"/{locale}/", link)
    return localed

def link_to_url(link, locale=""):
    domain= "https://developer.mozilla.org/"
    localed=link
    if locale:
        localed=locale_link(link, locale)
    return domain+localed


# %%
ele_des_dict = {
    "element" : ({
        "ja": "要素",
        "en-US": "Element",
        "fr"   : "Élément",
        "ko"   : "요소",
        "ru"   : "Элемент",
        "zh-CN": "元素",
        "zh-cn": "元素",
    }),
    "description" : ({
        "ja": "説明",
        "en-US": "Description",
        "ko"   : "설명",
        "ru"   : "Описание",
        "zh-CN": "描述",
        "zh-cn": "描述",
    }),
}

# %%
flatten_tags = [tag for tags in section_tag_lists for tag in tags]

ltd_mds = ("""\
{{HTMLElement("html")}}
{{HTMLElement("base")}} 
{{HTMLElement("head")}} 
{{HTMLElement("link")}} 
{{HTMLElement("meta")}} 
{{HTMLElement("style")}}
{{HTMLElement("title")}}
{{HTMLElement("body")}}
{{HTMLElement("address")}}                                                                                                                                                                                                                                                                                                                          
{{HTMLElement("article")}}                                                                                                                                                                                                                                                                                                                          
{{HTMLElement("aside")}}                                                                                                                                                                                                                                                                                                                            
{{HTMLElement("footer")}}                                                                                                                                                                                                                                                                                                                           
{{HTMLElement("header")}}                                                                                                                                                                                                                                                                                                                           
[`<h1>`](/en-US/docs/Web/HTML/Element/Heading_Elements), [`<h2>`](/en-US/docs/Web/HTML/Element/Heading_Elements), [`<h3>`](/en-US/docs/Web/HTML/Element/Heading_Elements), [`<h4>`](/en-US/docs/Web/HTML/Element/Heading_Elements), [`<h5>`](/en-US/docs/Web/HTML/Element/Heading_Elements), [`<h6>`](/en-US/docs/Web/HTML/Element/Heading_Elements)
{{HTMLElement("main")}}                                                                                                                                                                                                                                                                                                                             
{{HTMLElement("nav")}}                                                                                                                                                                                                                                                                                                                              
{{HTMLElement("section")}}                                                                                                                                                                                                                                                                                                                          
{{HTMLElement("blockquote")}}
{{HTMLElement("dd")}}        
{{HTMLElement("div")}}       
{{HTMLElement("dl")}}        
{{HTMLElement("dt")}}        
{{HTMLElement("figcaption")}}
{{HTMLElement("figure")}}    
{{HTMLElement("hr")}}        
{{HTMLElement("li")}}        
{{HTMLElement("menu")}}      
{{HTMLElement("ol")}}        
{{HTMLElement("p")}}         
{{HTMLElement("pre")}}       
{{HTMLElement("ul")}}        
{{HTMLElement("a")}}     
{{HTMLElement("abbr")}}  
{{HTMLElement("b")}}     
{{HTMLElement("bdi")}}   
{{HTMLElement("bdo")}}   
{{HTMLElement("br")}}    
{{HTMLElement("cite")}}  
{{HTMLElement("code")}}  
{{HTMLElement("data")}}  
{{HTMLElement("dfn")}}   
{{HTMLElement("em")}}    
{{HTMLElement("i")}}     
{{HTMLElement("kbd")}}   
{{HTMLElement("mark")}}  
{{HTMLElement("q")}}     
{{HTMLElement("rp")}}    
{{HTMLElement("rt")}}    
{{HTMLElement("ruby")}}  
{{HTMLElement("s")}}     
{{HTMLElement("samp")}}  
{{HTMLElement("small")}} 
{{HTMLElement("span")}}  
{{HTMLElement("strong")}}
{{HTMLElement("sub")}}   
{{HTMLElement("sup")}}   
{{HTMLElement("time")}}  
{{HTMLElement("u")}}     
{{HTMLElement("var")}}   
{{HTMLElement("wbr")}}   
{{HTMLElement("area")}} 
{{HTMLElement("audio")}}
{{HTMLElement("img")}}  
{{HTMLElement("map")}}  
{{HTMLElement("track")}}
{{HTMLElement("video")}}
{{HTMLElement("embed")}}  
{{HTMLElement("iframe")}} 
{{HTMLElement("object")}} 
{{HTMLElement("picture")}}
{{HTMLElement("portal")}} 
{{HTMLElement("source")}} 
{{SVGElement("svg")}}    
{{MathMLElement("math")}}
{{HTMLElement("canvas")}}  
{{HTMLElement("noscript")}}
{{HTMLElement("script")}}  
{{HTMLElement("del")}}
{{HTMLElement("ins")}}
{{HTMLElement("caption")}} 
{{HTMLElement("col")}}     
{{HTMLElement("colgroup")}}
{{HTMLElement("table")}}   
{{HTMLElement("tbody")}}   
{{HTMLElement("td")}}      
{{HTMLElement("tfoot")}}   
{{HTMLElement("th")}}      
{{HTMLElement("thead")}}   
{{HTMLElement("tr")}}      
{{HTMLElement("button")}}  
{{HTMLElement("datalist")}}
{{HTMLElement("fieldset")}}
{{HTMLElement("form")}}    
{{HTMLElement("input")}}   
{{HTMLElement("label")}}   
{{HTMLElement("legend")}}  
{{HTMLElement("meter")}}   
{{HTMLElement("optgroup")}}
{{HTMLElement("option")}}  
{{HTMLElement("output")}}  
{{HTMLElement("progress")}}
{{HTMLElement("select")}}  
{{HTMLElement("textarea")}}
{{HTMLElement("details")}}
{{HTMLElement("dialog")}} 
{{HTMLElement("summary")}}
{{HTMLElement("slot")}}    
{{HTMLElement("template")}}
{{HTMLElement("acronym")}}  
{{HTMLElement("applet")}}   
{{HTMLElement("bgsound")}}  
{{HTMLElement("big")}}      
{{HTMLElement("blink")}}    
{{HTMLElement("center")}}   
{{HTMLElement("content")}}  
{{HTMLElement("dir")}}      
{{HTMLElement("font")}}     
{{HTMLElement("frame")}}    
{{HTMLElement("frameset")}} 
{{HTMLElement("image")}}    
{{HTMLElement("keygen")}}   
{{HTMLElement("marquee")}}  
{{HTMLElement("menuitem")}} 
{{HTMLElement("nobr")}}     
{{HTMLElement("noembed")}}  
{{HTMLElement("noframes")}} 
{{HTMLElement("param")}}    
{{HTMLElement("plaintext")}}
{{HTMLElement("rb")}}       
{{HTMLElement("rtc")}}      
{{HTMLElement("shadow")}}   
{{HTMLElement("spacer")}}   
{{HTMLElement("strike")}}   
{{HTMLElement("tt")}}       
{{HTMLElement("xmp")}}      
""").splitlines()

tad_to_ltd_md = {tag: md for tag, md in zip(flatten_tags, ltd_mds)}
tag_to_index = {tag: i for i, tag in enumerate(flatten_tags)}
len(flatten_tags), len(ltd_mds)

# %%
def link_to_path(link, locale):
    #      /ja/docs/Web/HTML/Element/html
    # files/ja/     web/html/element/html/index.md
    localed = locale_link(link, locale).replace("/docs/", "/")
    return f"files{localed}/index.md".lower()

# %%
import os
lower_locale_to_normal = {
    "pt-br": "pt-BR",
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",
}
def convert_link_to_locale_link(md, locale: str):
    #      /ja/docs/Web/HTML/Element/html
    replacing = locale
    for key in lower_locale_to_normal.keys():
        replacing = re.sub(key, lambda m: lower_locale_to_normal[m[0]], replacing)
    normal_case_locale = replacing
    founds = re.findall(r"(\[([^\]]*)\]\(([^)]+)\))", md)
    for found in founds:
        full, text, link = found
        if re.search("^/"+locale+"/", link, flags=re.I):continue
        if os.path.exists(link_to_path(link, locale.lower())):
            localed_link = locale_link(link, normal_case_locale)
            localed_full = full.replace(link, localed_link)
            md = md.replace(full, localed_full)
    return md

# %%
def summary_to_md_line(tag, summary, defaulttag=""):
    ltdmd = tad_to_ltd_md.get(tag, defaulttag)
    rtdmd = summary if summary else enus_summaries[tag_to_index[tag]]
    return f"| {ltdmd} | {rtdmd} |"

def summaries_to_md_table(tags, summaries, locale):
    element = ele_des_dict["element"].get(locale, "Element")
    description = ele_des_dict["description"].get(locale, "Description")
    elelen = len(element) if len(element) > 3 else 4
    deslen = len(description) if len(description) > 3 else 4
    header = (
        "| "
        + element
        + " | "
        + description
        + " |"
    ) + "\n| " + ("-" * elelen) + " | " + ("-" * deslen) + " |\n"
    lines = [summary_to_md_line(*args) for args in zip(tags, summaries)]
    body = "".join([line + "\n" for line in lines])
    return header + body

locale_to_mdtables = {}
for locale, summaries in summaries_f_localedict.items():
    tag_to_summary = {tag: summary for summary, tag in zip(summaries, flatten_tags)}
    md_tables = []
    for section_tags in section_tag_lists:
        section_summaries = [tag_to_summary[tag] for tag in section_tags]
        md_table = summaries_to_md_table(section_tags, section_summaries, locale)
        md_tables.append(md_table)
    locale_to_mdtables[locale] = md_tables

locale_to_mdtables

# %%
replacees = [
"""{{HTMLRefTable("HTML Root Element")}}\n""",
"""{{HTMLRefTable("HTML Document Metadata")}}\n""",
"""{{HTMLRefTable("Sectioning Root Element")}}\n""",
"""{{HTMLRefTable("HTML Sections")}}\n""",
"""{{HTMLRefTable("HTML Grouping Content")}}\n""",
"""{{HTMLRefTable("HTML Text-Level Semantics")}}\n""",
"""{{HTMLRefTable("multimedia")}}\n""",
"""{{HTMLRefTable({"include":["HTML embedded content"], "exclude":["multimedia"]})}}\n""",
"""{{HTMLRefTable("HTML Scripting")}}\n""",
"""{{HTMLRefTable("HTML Edits")}}\n""",
"""{{HTMLRefTable("HTML tabular data")}}\n""",
"""{{HTMLRefTable({"include": ["HTML forms"], "exclude":["Deprecated"]})}}\n""",
"""{{HTMLRefTable("HTML interactive elements")}}\n""",
"""{{HTMLRefTable({"include":["Web Components"],"exclude":["Deprecated", "Obsolete"]})}}\n""",
"""{{HTMLRefTable({"include":["Deprecated","Obsolete"]})}}\n""",
]
replacee_patterns = [re.escape(s) for s in replacees]

# %%
def replace_macro(locale):
    with open(link_to_path("/en-US/docs/Web/HTML/Element", locale)) as f:
        source = f.read()
    replacing = source
        
    macro_pattern = r"^\{\{HTMLRefTable([^}]*|[^}]*\{[^}]+\}[^}]*)\}\}$"
    macronum = len(re.findall(macro_pattern, source, re.M))
    # if macronum != 15:
    #     raise Exception(macronum)
    
    failedcount = 0
    mdtables = locale_to_mdtables[locale]
    mdtables_without_svg = mdtables[:8] + mdtables[9:]
    for i, (replacee, mdtable) in enumerate(zip(replacees, mdtables_without_svg)):
        old = replacing
        #replacing = replacing.replace(replacee, mdtable, 1)
        replacing = re.sub(replacee_patterns[i], mdtable, replacing, count=1, flags=re.I)
        if old == replacing:
            failedcount += 1
            if failedcount > 1:
                raise Exception(replacing)
    
    old = replacing
    replacing = convert_link_to_locale_link(replacing, locale)
    if old!=replacing:
        pass#print("######"+old+ "######"+replacing)
    
    old = replacing
    before_pattern = r"""<table class="no-markdown">((?!</table>)(.|\n))+</table>\n"""
    replacing = re.sub(before_pattern, mdtables[8], replacing, count=1)
    if old == replacing:
        raise Exception(replacing)
    
    return replacing
    
for locale in locales:
    try:
        s=replace_macro(locale.lower())
        print("            ", locale, ":", "success")
    except Exception as e:
       print(locale, ":", "failed")#, e)
    

# %%
import os
# os.system("code " + link_to_path("/en-US/docs/Web/HTML/Element", "en-US"))
# os.system("code " + link_to_path("/ja/docs/Web/HTML/Element", "ja"))
# os.system("code " + link_to_path("/es/docs/Web/HTML/Element", "es"))
# os.system("code " + link_to_path("/fr/docs/Web/HTML/Element", "fr"))
# os.system("code " + link_to_path("/ko/docs/Web/HTML/Element", "ko"))
# os.system("code " + link_to_path("/pt-BR/docs/Web/HTML/Element", "pt-BR"))
# os.system("code " + link_to_path("/ru/docs/Web/HTML/Element", "ru"))
# os.system("code " + link_to_path("/zh-CN/docs/Web/HTML/Element", "zh-CN"))
# os.system("code " + link_to_path("/zh-TW/docs/Web/HTML/Element", "zh-TW"))

# %%
def replace_macro_and_write(locale):
    replaced = replace_macro(locale.lower())
    with open(link_to_path("/en-US/docs/Web/HTML/Element", locale), "w", encoding="utf-8") as f:
        f.write(replaced)
        
# replace_macro_and_write("ja")
# replace_macro_and_write("es")
# replace_macro_and_write("fr")
# replace_macro_and_write("ko")
# replace_macro_and_write("pt-BR")
# replace_macro_and_write("ru")
# replace_macro_and_write("zh-CN")
# replace_macro_and_write("zh-TW")


# %% [markdown]
# # 以下、一時コード（WayBackMachine 関連）

# %%
import json
urls=["https://developer.mozilla.org/es/docs/Web/HTML/Element",
"https://developer.mozilla.org/fr/docs/Web/HTML/Element",
"https://developer.mozilla.org/ja/docs/Web/HTML/Element",
"https://developer.mozilla.org/ko/docs/Web/HTML/Element",
"https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element",
"https://developer.mozilla.org/ru/docs/Web/HTML/Element",
"https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element",
"https://developer.mozilla.org/zh-TW/docs/Web/HTML/Element",]
jsurls=[]
"""for url in urls:
    wbmurl="http://archive.org/wayback/available?url="+url
    res=requests.get(wbmurl)
    text=(res.text)
    js=json.loads(text)
    jsurl=js["archived_snapshots"]["closest"]["url"]
    print(jsurl)
    jsurls.append(jsurl)"""
jsurls=[
    "http://web.archive.org/web/20221209144013/https://developer.mozilla.org/es/docs/Web/HTML/Element",
    "http://web.archive.org/web/20230214020459/https://developer.mozilla.org/fr/docs/Web/HTML/Element",
    "http://web.archive.org/web/20230203235743/https://developer.mozilla.org/ja/docs/Web/HTML/Element",
    "http://web.archive.org/web/20221215193922/https://developer.mozilla.org/ko/docs/Web/HTML/Element",
    "http://web.archive.org/web/20230115140446/https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element",
    "http://web.archive.org/web/20221214131651/https://developer.mozilla.org/ru/docs/Web/HTML/Element",
    "http://web.archive.org/web/20221209203824/https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element",
    "http://web.archive.org/web/20221210235550/https://developer.mozilla.org/zh-TW/docs/Web/HTML/Element",
]
archiveds=[]#requests.get(url) for url in jsurls]

# %%
ltd_textss=[]
s=""
for i, archive in enumerate(archiveds):
    txt = archive.text
    ltds=bs4.BeautifulSoup(txt).select("main#content td[style]")
    ltd_texts=[ltd.text for ltd in ltds]
    ltd_textss.append(ltd_texts)
    print(len(ltds))
    s+="\t".join(ltd_texts)+"\n"



