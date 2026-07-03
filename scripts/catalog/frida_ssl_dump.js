// Frida hook v3 — Windows Schannel(SSPI)明文截获。
// WBox 的 HTTPS(→114.80.154.45)走 Schannel,不是 OpenSSL。明文出现在 SSPI 的:
//   EncryptMessage(ctx, fQOP, pMessage, seq)  —— onEnter 时 SECBUFFER_DATA=明文请求
//   DecryptMessage(ctx, pMessage, seq, pfQOP) —— onLeave 时 SECBUFFER_DATA=明文响应
// 用 CtxtHandle(两个指针)做 per-连接关联,只留发往目标主机那条连接。

'use strict';
var TARGET = 'wind.com.cn', TARGET_IP = '114.80.154.45', MAXBUF = 262144;

// —— 跨 frida 版本解析全局导出 ——
function resolve(name) {
  try { if (Module.getGlobalExportByName) return Module.getGlobalExportByName(name); } catch (e) {}
  try { var p = Module.getExportByName(null, name); if (p && !p.isNull()) return p; } catch (e) {}
  var r = null;
  Process.enumerateModules().forEach(function (m) {
    if (r) return;
    try {
      var mod = Process.getModuleByName ? Process.getModuleByName(m.name) : null;
      var q = (mod && mod.getExportByName) ? mod.getExportByName(name) : Module.getExportByName(m.name, name);
      if (q && !q.isNull()) r = q;
    } catch (e) {}
  });
  return r;
}

function s(bytes, n) { var o = ''; n = Math.min(bytes.length, n || bytes.length); for (var i = 0; i < n; i++) o += String.fromCharCode(bytes[i]); return o; }
function isHttpReq(pv, cb) { return /^(GET|POST|PUT|HEAD|DELETE|OPTIONS) /.test(s(new Uint8Array(Memory.readByteArray(pv, Math.min(cb, 8))))); }
function head(pv, cb) { return s(new Uint8Array(Memory.readByteArray(pv, Math.min(cb, 2048))), 2048); }

function ctxKey(pCtx) {
  try { return pCtx.readU64().toString() + ':' + pCtx.add(8).readU64().toString(); } catch (e) { return 'x'; }
}
// SecBufferDesc: ulVersion(4) cBuffers(4) pBuffers(8@off8)
// SecBuffer[x64]: cbBuffer(4) BufferType(4) pvBuffer(8) = 16
function eachDataBuf(pDesc, cb) {
  if (pDesc.isNull()) return;
  var cn = pDesc.add(4).readU32(), pb = pDesc.add(8).readPointer();
  for (var i = 0; i < cn && i < 16; i++) {
    var e = pb.add(i * 16), len = e.readU32(), ty = e.add(4).readU32(), pv = e.add(8).readPointer();
    if (ty === 1 /*SECBUFFER_DATA*/ && len > 0 && !pv.isNull()) cb(pv, len);
  }
}

var interesting = {};
var pEnc = resolve('EncryptMessage'), pDec = resolve('DecryptMessage');
send({ t: 'info', msg: 'EncryptMessage=' + (pEnc ? pEnc : 'null') + ' DecryptMessage=' + (pDec ? pDec : 'null') });

var encN = 0, decN = 0, reqN = 0, hosts = {};
setInterval(function () { send({ t: 'info', msg: 'stat enc=' + encN + ' dec=' + decN + ' httpReq=' + reqN + ' hosts=' + JSON.stringify(Object.keys(hosts)) }); }, 8000);

if (pEnc) Interceptor.attach(pEnc, {
  onEnter: function (a) {
    encN++;
    var key = ctxKey(a[0]);
    eachDataBuf(a[2], function (pv, len) {
      if (isHttpReq(pv, len)) {
        reqN++;
        var h = head(pv, len);
        var mh = /Host:\s*([^\r\n]+)/i.exec(h); if (mh) hosts[mh[1].trim()] = 1;
        interesting[key] = true;   // 任何 HTTP 连接都留,便于诊断
        send({ t: 'req', ssl: key, len: Math.min(len, MAXBUF) }, Memory.readByteArray(pv, Math.min(len, MAXBUF)));
      }
    });
  }
});

if (pDec) Interceptor.attach(pDec, {
  onEnter: function (a) { decN++; this.key = ctxKey(a[0]); this.pMsg = a[1]; },
  onLeave: function () {
    if (!interesting[this.key]) return;
    var self = this;
    eachDataBuf(this.pMsg, function (pv, len) {
      send({ t: 'resp', ssl: self.key, len: Math.min(len, MAXBUF) }, Memory.readByteArray(pv, Math.min(len, MAXBUF)));
    });
  }
});

send({ t: 'info', msg: 'schannel hooks: enc=' + (!!pEnc) + ' dec=' + (!!pDec) });
