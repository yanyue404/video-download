// ==UserScript==
// @name 飞书优化
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @include https://*.feishu.cn/*
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';

    // 背景色护眼模式

    GM_addStyle("html,body, #mainBox, .app, .suite-body,  .navigation-bar.navigation-bar__suite, .doc-comment-v2,.catalogue__list {background-color: #C7EDCC !important} .section-nav-container .full-entry-title { background: none !important}")

    // watermark 移除

    GM_addStyle(".suite-clear { display: none !important}")

})();
