function randomId($t, Wt) {
    isStr$2($t) && (Wt = $t),
    isNum$4($t) || ($t = 12);
    var rr = "";
    !Wt || !isStr$2(Wt) ? rr = charNb + charUpper : Wt === "[*]" ? rr = charNb + charLower + charUpper + charSpecial : Wt.match(/0-9|a-z|A-Z|\[s\]/) ? (/0-9/.test(Wt) && (rr += charNb),
    /a-z/.test(Wt) && (rr += charLower),
    /A-Z/.test(Wt) && (rr += charUpper),
    /\[s\]/.test(Wt) && (rr += charSpecial),
    rr += unique(Wt.replace(/0-9|a-z|A-Z|\[s\]/g, ""))) : rr = Wt;
    for (var en = "", rn = -1; ++rn < $t; )
        en += rr[randomNum(rr.length)];
    return en
}
function isNum$4($t, Wt) {
    var rr = typeof $t == "number";
    return Wt ? rr : rr && !Number.isNaN($t) && Number.isFinite($t)
}
function isStr$2($t) {
    return typeof $t == "string"
}
var ID_CHAR_SET = {
    number: "0123456789",
    letter: "abcdefghijklmnopqrstuvwxyz",
    special: "~`!@#$%^&*()-_+=[]{};:\"',<.>/?"
}
  , RE_DB_CHAR = /^[^x00-xff]*$/;
var charNb = ID_CHAR_SET.number
  , charLower = ID_CHAR_SET.letter
  , charUpper = charLower.toUpperCase()
  , charSpecial = ID_CHAR_SET.special;
function isArr($t) {
    return $t instanceof Array
}
function randomNum($t, Wt, rr) {
    var en = Math.random();
    if (!isNum$4($t))
        return en;
    isBol(Wt) && (rr = Wt);
    var rn;
    return !isNum$4(Wt) || Wt === $t ? rn = en * $t : rn = en * (Wt - $t) + $t,
    rr ? rn : Math.floor(rn)
}
function isBol($t) {
    return typeof $t == "boolean"
}
function unique($t, Wt) {
    var rr = isStr$2($t);
    rr && ($t = $t.split("")),
    isArr($t) || ($t = []);
    for (var en = $t.slice(), rn = -1; ++rn < en.length; )
        for (var on = rn, an = function() {
            var mn = en[rn]
              , gn = en[on]
              , bn = isArr(Wt)
              , An = !bn && (Wt ? mn == gn : mn === gn) || bn && Wt.some(function(Tn) {
                return mn && gn && !isUdf(mn[Tn]) && mn[Tn] === gn[Tn]
            });
            An && en.splice(on--, 1)
        }; ++on < en.length; )
            an();
    return rr ? en.join("") : en
}
function getqvId(){
    return randomId(32, "0-9a-zA-Z");
}
// const res = randomId(32, "0-9a-zA-Z")

// console.log(res)