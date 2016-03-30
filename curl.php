<?php

$url = "http://www.darklyrics.com/lyrics/aaaarrghh/lmkadarsouklkadarsoluk.html";

$ch = curl_init();
// 设置浏览器的特定header
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
                                           "www.darklyrics.com",
                                           "Connection: keep-alive",
                                           "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                           "Upgrade-Insecure-Requests: 1",
                                           "DNT:1",
                                           "Accept-Language: zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4,en-US;q=0.2",
                                           'Cookie:DJ_UVID=MTQ0MDA0OTAxMDE1MTQ1MDcy; dj_auth_v3=MRwvnp6ln4O1mVZuM6zjhFDKaqdRXoIAHPk1OHfFS4TyC7O-zZw315HWnS0ayQM*; uchome_loginuser=28385971; login_email=898150165%40qq.com; DJ_RF=empty; DJ_EU=http%3A%2F%2Fm.dajie.com%2Fdict%2Fcity%3FparentId%3D0',
                                           ));
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0');
// 在HTTP请求头中"Referer: "的内容。
curl_setopt($ch, CURLOPT_REFERER,"https://www.baidu.com");
curl_setopt($ch, CURLOPT_ENCODING, "gzip, deflate, sdch");
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_TIMEOUT,120);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);//302redirect

$html = curl_exec($ch);
curl_close($ch);
if($html === false) {
    echo 'Curl error: ' . curl_error($ch) . "<br>\n\r";
} else {
    echo $html;
}

?>