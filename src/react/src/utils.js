
/* take ms value as input and return a string of MM:SS */
export function toTimeStr(ms) {
    const totseconds = (ms / 1000);
    const m = Math.round(totseconds / 60);
    const s = Math.floor(totseconds % 60).toString().padStart(2,'0')
    return `${m}:${s}`;
}
