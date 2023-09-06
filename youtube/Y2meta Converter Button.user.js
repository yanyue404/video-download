// ==UserScript==
// @name        Y2meta Converter Button
// @namespace   https://y2meta.com/
// @version     1.5
// @date        2019-07-23
// @author      Max
// @description Y2meta Downloader: Download Video and Audio for free
// @homepage    https://y2meta.com/
// @icon        https://y2meta.com/imgs/logo.png
// @icon64      https://y2meta.com/imgs/logo.png
// @updateURL   https://y2meta.com/extensions/chrome/helper.meta.js
// @downloadURL https://y2meta.com/extensions/chrome/helper.user.js
// @include     http://*
// @include     https://*
// @run-at      document-end
// @grant       GM_listValues
// @grant       GM_setValue
// @grant       GM_getValue
// @grant       GM_deleteValue
// @grant       GM_xmlhttpRequest
// @grant       GM_info
// @grant       GM_openInTab
// @grant       GM_setClipboard
// @grant       GM_registerMenuCommand
// @grant       GM_unregisterMenuCommand
// @grant       GM_notification
// @grant       GM_download
// @grant       GM.info
// @grant       GM.listValues
// @grant       GM.setValue
// @grant       GM.getValue
// @grant       GM.deleteValue
// @grant       GM.openInTab
// @grant       GM.setClipboard
// @grant       GM.xmlHttpRequest
// @connect     youtube.com
// @connect     m.youtube.com
// @connect     www.youtube.com
// @connect     youtube-nocookie.com
// @connect     youtu.be
// @connect     y2meta.com
// @connect     self
// @connect     *
// ==/UserScript==
var MaxMain = {
  oXHttpReq: null,
  vid: null,
  oldUrl: null,
  DocOnLoad: function (o) {
    try {
      if (
        null != o &&
        null != o.body &&
        null != o.location &&
        ((MaxMain.vid = MaxMain.getVid(o)), MaxMain.vid)
      ) {
        o.querySelector("#info-contents #info").setAttribute(
          "style",
          "flex-wrap: wrap;"
        );
        var t = o.querySelector("#above-the-fold #menu"),
          e = o.querySelector("#y2metaconverter"),
          n = MaxMain.GetCommandButton();
        t.parentNode.insertBefore(n, t),
          (MaxMain.oldUrl = o.location.href),
          MaxMain.checkChangeVid();
      }
      return !0;
    } catch (o) {
      console.log("Ошибка в функции Y2meta.DocOnLoad. ", o);
    }
  },
  checkChangeVid: function () {
    setTimeout(function () {
      MaxMain.oldUrl == window.location.href
        ? MaxMain.checkChangeVid()
        : MaxMain.WaitLoadDom(window.document);
    }, 1e3);
  },
  WaitLoadDom: function (o) {
    (MaxMain.vid = MaxMain.getVid(o)),
      MaxMain.vid
        ? null != o.querySelector("#above-the-fold #menu")
          ? MaxMain.DocOnLoad(o)
          : setTimeout(function () {
              MaxMain.WaitLoadDom(o);
            }, 1e3)
        : MaxMain.checkChangeVid();
  },
  goToY2meta: function (o) {
    try {
      var t =
        "https://www.y2meta.com/youtube/" +
        MaxMain.vid +
        "/?utm_source=chrome_addon";
      window.open(t, "_blank");
    } catch (o) {
      console.log("Ошибка в функции Y2meta.OnButtonClick. ", o);
    }
  },
  GetCommandButton: function () {
    try {
      var o = document.createElement("button");
      return (
        (o.id = "y2metaconverter"),
        (o.className = "yt-uix-tooltip"),
        o.setAttribute("type", "button"),
        o.setAttribute("title", "Download with y2meta.com"),
        (o.innerHTML = "Download"),
        o.addEventListener(
          "click",
          function (o) {
            MaxMain.goToY2meta(o);
          },
          !0
        ),
        o.setAttribute(
          "style",
          "min-height:25px; position:relative; top:1px; cursor: pointer; font: 13px Arial; background: #ff003e; color: #fff; text-transform: uppercase; display: block; padding: 10px 16px; margin: 20px 5px 10px 5px; border: 1px solid #ff0068; border-radius: 2px; font-weight:bold"
        ),
        o.setAttribute("onmouseover", "this.style.backgroundColor='#c10841'"),
        o.setAttribute("onmouseout", "this.style.backgroundColor='#ff003e'"),
        o
      );
    } catch (o) {
      console.log("Ошибка в функции Y2meta.GetCommandButton. ", o);
    }
  },
  getVid: function (o) {
    var t = o.location
      .toString()
      .match(
        /^.*((m\.)?youtu\.be\/|vi?\/|u\/\w\/|embed\/|\?vi?=|\&vi?=)([^#\&\?]*).*/
      );
    return !(!t || !t[3]) && t[3];
  },
};
MaxMain.WaitLoadDom(window.document);
