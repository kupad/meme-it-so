<?php
//point a server like nginx to this PHP instead of index.html and it can do substitutions before delivering the index.html content
//good for  meta-tags that really change (for social media links / seo) even though we're delivering a SPA

//right now just: 
//PHP_HOOK gets replaced with the contents in phphook.txt. This isn't really a very efficient way to do the replace, since 
//it's done on every request. sed would do nicely for this.
$hookid = '<!-- PHP_HOOK  -->';
$replace= file_get_contents('phphook.txt');
$html = file_get_contents('index.html');
echo str_replace($hookid, $replace, $html);

?>
