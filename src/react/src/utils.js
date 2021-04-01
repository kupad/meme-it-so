
/* take ms value as input and return a string of MM:SS */
export function toTimeStr(ms) {
    const totseconds = (ms / 1000);
    const m = Math.round(totseconds / 60);
    const s = Math.floor(totseconds % 60).toString().padStart(2,'0')
    return `${m}:${s}`;
}

/*
b64 encode string s using the URL and filesystem-safe alphabet, which substitutes - instead of + and _ instead of / in the standard Base64 alphabet,
*/
export function urlsafe_btoa(s) {
    return btoa(s).replace('+', '-').replace('/','_');
}
