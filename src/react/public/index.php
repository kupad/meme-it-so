<?php
//point a server like nginx to this PHP instead of index.html and it can do substitutions before delivering the index.html content
//good for  meta-tags that really change (for social media links / seo) even though we're delivering a SPA

//full html
$html = file_get_contents('index.html');

//phphook gets replaced with the contents in phphook.txt. This isn't really a very efficient way to do the replace, since
//it's done on every server-side app request. sed would do nicely for this.
$phphookid = '<script class="PHP_HOOK"></script>';
$phphook_replace= file_get_contents('phphook.txt');
$html = str_replace($phphookid, $phphook_replace, $html);

$socialimagehook= '__SOCIAL_IMAGE__';
$socialimage_replace = file_get_contents('socialimage.txt');
$html = str_replace($socialimagehook, $socialimage_replace, $html);

//echo out the modified html
echo $html;

?>
